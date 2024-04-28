import logging
from database import session, History, Person, Position, Location, Road, Region, TrafficHistory
from .schemas import TrafficData
from settings import cache
from sqlalchemy import and_
from sqlalchemy.orm import aliased

__all__ = ["calculate_traffic_function"]

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def _calculate_traffic_for_road(road: Road) -> int:
    calculated_rate = round(
        ((len(road.people) / road.max_num_of_cars)
         + ((road.max_speed - road.average_speed) / road.max_speed)) / 2
        * 10
    )
    calculated_rate = max(0, calculated_rate)
    return calculated_rate


def calculate_traffic_function(traffic_schema: dict):
    traffic_data = TrafficData(**traffic_schema)
    # ----- traffic calculation logic -----
    try:
        with session.begin():
            # Create aliases for Position table
            StartPosition = aliased(Position)
            EndPosition = aliased(Position)

            # Execute the query
            approximate_road_location = session.query(Road). \
                join(StartPosition, Road.start_position == StartPosition.id). \
                join(EndPosition, Road.end_position == EndPosition.id). \
                filter(
                and_(
                    StartPosition.latitude <= traffic_data.traffic_data.location.latitude,
                    StartPosition.longitude <= traffic_data.traffic_data.location.longitude,
                    EndPosition.latitude >= traffic_data.traffic_data.location.latitude,
                    EndPosition.longitude >= traffic_data.traffic_data.location.longitude,
                )
            ).first()
            if approximate_road_location is None:
                raise Exception("Unknown road")

            person_location = Location(
                latitude=traffic_data.traffic_data.location.latitude,
                longitude=traffic_data.traffic_data.location.longitude
            )

            session.add(person_location)
            person_location = session.query(Location).filter_by(
                latitude=person_location.latitude,
                longitude=person_location.longitude
            ).first()

            person = session.get(Person, traffic_data.person_id)
            if person is None:
                person = Person(
                    id=traffic_data.person_id,
                    current_road_id=approximate_road_location.id,
                    current_speed=traffic_data.traffic_data.speed,
                    current_location_id=person_location.id
                )
                session.add(person)
            else:
                person.current_road_id = approximate_road_location.id
                person.current_speed = traffic_data.traffic_data.speed
                person.current_location_id = person_location.id

            history = History(
                timestamps=traffic_data.traffic_data.timestamp,
                person_id=person.id,
                location_id=person_location.id
            )
            session.add(history)

            previous_road_location = cache.get(f"{traffic_data.person_id}-current-road")

            logger.info("Previous road location: %s", previous_road_location)

            if previous_road_location is not None:
                if int(previous_road_location.decode("utf-8")) != approximate_road_location.id:
                    prev_road = session.get(Road, previous_road_location.decode("utf-8"))
                    logger.info("Previous road location is not None")
                    try:
                        av_speed = sum([p.current_speed for p in prev_road.people]) / len(prev_road.people)
                    except ZeroDivisionError:
                        av_speed = 0
                    prev_road.average_speed = av_speed
                    calculated_rate = _calculate_traffic_for_road(prev_road)
                    logger.info("Calculated rate: %s", calculated_rate)
                    logger.info(prev_road.people)
                    prev_road.traffic_rate = calculated_rate
                    traffic_history = TrafficHistory(
                        timestamp=traffic_data.traffic_data.timestamp,
                        road_id=prev_road.id,
                        average_speed=prev_road.average_speed,
                        traffic_rate=prev_road.traffic_rate
                    )
                    session.add(traffic_history)

            cache.set(f"{traffic_data.person_id}-current-road", int(approximate_road_location.id))

            av_speed = sum([p.current_speed for p in approximate_road_location.people]) / len(
                approximate_road_location.people)
            approximate_road_location.average_speed = av_speed
            calculated_rate = _calculate_traffic_for_road(approximate_road_location)
            approximate_road_location.traffic_rate = calculated_rate
            logger.info("Calculated rate: %s", calculated_rate)
            logger.info(approximate_road_location.people)

            traffic_history = TrafficHistory(
                timestamp=traffic_data.traffic_data.timestamp,
                road_id=approximate_road_location.id,
                average_speed=approximate_road_location.average_speed,
                traffic_rate=approximate_road_location.traffic_rate
            )
            session.add(traffic_history)
            logger.info("Traffic calculated successfully for person %s", traffic_data.person_id)
    except Exception as e:
        logger.warning("Error occurred while calculating traffic", e)
