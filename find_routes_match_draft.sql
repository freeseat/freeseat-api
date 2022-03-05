DROP TABLE driver_route;
CREATE TABLE driver_route
(
    name                 VARCHAR,
    max_deviation_meters REAL,
    route                geometry(LineString, 4326)
);

INSERT INTO driver_route(name, max_deviation_meters, route)
VALUES ('1', 5000,
        ST_GeomFromGeoJSON('{"type":"LineString","coordinates":[[23.4942626953125,51.13455469147683],[22.56591796875,51.25847731518399],[21.851806640625,51.570241445811234],[21.000366210937496,52.2378923494213],[20.36865234375,53.12040528310657]]}')),
       ('2', 5000,
        ST_GeomFromGeoJSON('{"type":"LineString","coordinates":[[23.4832763671875,51.13455469147683],[22.8955078125,51.64188525876834],[22.3846435546875,51.940878612558684],[22.2857666015625,52.17056279155013],[21.5386962890625,52.18403686498285],[20.9783935546875,52.24125614966341],[19.9237060546875,52.1098789403549],[19.423828125,51.781435604431195]]}')),
       ('3', 10000,
        ST_GeomFromGeoJSON('{"type":"LineString","coordinates":[[22.730712890625,50.534380406110806],[23.280029296875,50.736455137010665],[23.48876953125,51.138001488062564],[22.785644531249996,51.984880139916626],[21.456298828125,52.6030475337285],[20.58837890625,52.90227586168308],[19.40185546875,53.26521293124656],[18.7646484375,53.51418452077113]]}'));

WITH
    query_routes                           AS (
        SELECT st_geomfromgeojson('{"type":"LineString","coordinates":[[23.48876953125,51.13110763758015],[22.049560546875,52.328625488430184],[20.302734375,53.00817326643286],[19.40185546875,53.25206880589411],[19.40185546875,54.15600109028491]]}') AS route
    ),
    closest_point_fractions                AS (
        SELECT driver_route.name                                                         AS driver_name,
               driver_route.route                                                        AS driver_route,
               driver_route.max_deviation_meters                                         AS driver_max_deviation_meters,
               query_routes.route                                                        AS query_route,
               ST_LineLocatePoint(driver_route.route, st_startpoint(query_routes.route)) AS closest_point_fraction
        FROM query_routes
             LEFT JOIN driver_route
             ON TRUE
    ),
    driver_effective_routes                AS (
        SELECT driver_name,
               ST_LineSubstring(driver_route, closest_point_fraction, 1) AS driver_route,
               driver_max_deviation_meters,
               query_route
        FROM closest_point_fractions
        WHERE st_distance(
                      st_startpoint(query_route)::geography,
                      ST_LineInterpolatePoint(driver_route, closest_point_fraction)::geography
                  ) < driver_max_deviation_meters
    ),
    driver_expanded_routes                 AS (
        SELECT driver_name,
               driver_route,
               st_buffer(
                       driver_route::geography,
                       driver_max_deviation_meters,
                       'endcap=flat join=round'
                   )::geometry AS driver_route_polygon,
               query_route
        FROM driver_effective_routes
    ),
    common_routes                          AS (
        SELECT driver_name,
               query_route,
               driver_route_polygon,
               st_intersection(driver_route_polygon, query_route) AS common_route
        FROM driver_expanded_routes
    ),
    common_routes_furthest_points          AS (
        SELECT driver_name,
               query_route,
               driver_route_polygon,
               common_route,
               st_endpoint(
                       st_geometryn(
                               common_route,
                               GREATEST(st_numgeometries(common_route) - 1, 1))
                   ) AS furthest_point
        FROM common_routes
    ),
    common_routes_furthest_point_fractions AS (
        SELECT driver_name,
               ST_LineLocatePoint(query_route, furthest_point) AS furthest_point_fraction
        FROM common_routes_furthest_points
    )


SELECT *
FROM common_routes_furthest_point_fractions
ORDER BY furthest_point_fraction DESC
