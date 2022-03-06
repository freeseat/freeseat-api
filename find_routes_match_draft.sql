CREATE OR REPLACE FUNCTION match_partial_trips(
    trip_ids uuid[],
    driver_route_polyline VARCHAR,
    driver_max_deviation_meters REAL
)
    RETURNS TABLE
            (
                result_trip_id uuid
            )
AS
$$
DECLARE
    driver_route      geography := st_linefromencodedpolyline(driver_route_polyline)::geography;
    driver_route_geom geometry  = driver_route::geometry;
BEGIN
    RETURN QUERY
        WITH
            trips_routes                    AS (
                SELECT id                             AS trip_id,
                       route                          AS trip_route,
                       route::geometry                AS trip_route_geom,
                       st_startpoint(route::geometry) AS trip_route_start
                FROM trips_trip
                WHERE id = ANY (trip_ids)
            ),

            -- trip so that route start is within deviation of driver route
            trips_within_deviation          AS (
                SELECT trip_id,
                       trip_route,
                       trip_route_geom,
                       trip_route_start
                FROM trips_routes
                WHERE ST_DWithin(driver_route, trip_route_start, driver_max_deviation_meters)
            ),

            driver_after_pickup_routes      AS (
                SELECT trip_id,
                       trip_route,
                       trip_route_geom,
                       ST_LineSubstring(
                               driver_route_geom,
                               ST_LineLocatePoint(driver_route_geom, trip_route_start),
                               1
                           ) AS driver_after_pickup_route
                FROM trips_within_deviation
            ),

            driver_after_pickup_polygons    AS (
                SELECT trip_id,
                       trip_route,
                       trip_route_geom,
                       st_buffer(
                               driver_after_pickup_route::geography,
                               driver_max_deviation_meters,
                               'endcap=flat join=round'
                           )::geometry AS driver_after_pickup_polygon
                FROM driver_after_pickup_routes
            ),

            common_routes                   AS (
                SELECT trip_id,
                       trip_route,
                       trip_route_geom,
                       st_intersection(driver_after_pickup_polygon, trip_route) AS common_route
                FROM driver_after_pickup_polygons
            ),

            common_routes_dropoff_points    AS (
                SELECT trip_id,
                       trip_route,
                       trip_route_geom,
                       st_endpoint(
                               st_geometryn(
                                       common_route::geometry,
                                       GREATEST(st_numgeometries(common_route::geometry), 1))
                           ) AS dropoff_point
                FROM common_routes
            ),
            common_routes_dropoff_fractions AS (
                SELECT trip_id,
                       ST_LineLocatePoint(trip_route_geom, dropoff_point) AS dropoff_fraction
                FROM common_routes_dropoff_points
            )

        SELECT trip_id
        FROM common_routes_dropoff_fractions
        WHERE dropoff_fraction IS NOT NULL
        ORDER BY dropoff_fraction DESC
        LIMIT 5;

END;
$$ LANGUAGE plpgsql STABLE;
