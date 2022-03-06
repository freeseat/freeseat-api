from apps.trips.enums import TripState
from apps.trips.models import TripProposal
from django.db import transaction

__all__ = ["TripProposalService"]


class TripProposalService:
    @classmethod
    @transaction.atomic
    def propose_trip(cls, data: dict) -> TripProposal:
        pass

    @classmethod
    @transaction.atomic
    def update_proposed_trip(
        cls, trip_request: TripProposal, data: dict
    ) -> TripProposal:
        pass

    @classmethod
    def _change_trip_proposal_state(
        cls, trip_request: TripProposal, to_state: TripState
    ) -> TripProposal:
        trip_request.state = to_state
        trip_request.save(update_fields=["state"])

        return trip_request

    @classmethod
    def cancel_proposed_trip(cls, trip_request: TripProposal) -> TripProposal:
        return cls._change_trip_proposal_state(trip_request, TripState.CANCELLED)

    @classmethod
    def complete_proposed_trip(cls, trip_request: TripProposal) -> TripProposal:
        return cls._change_trip_proposal_state(trip_request, TripState.COMPLETED)
