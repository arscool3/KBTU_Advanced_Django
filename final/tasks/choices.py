import enum


class StatusEnum(enum.Enum):
    OPEN = "OPEN"
    DEV_ANALYSIS = "DEV_ANALYSIS"
    DEV_ANALYSIS_DONE = "DEV_ANALYSIS_DONE"
    DEV_DOING = "DEV_DOING"
    DEV_DONE = "DEV_DONE"
    TEST_DOING = "TEST_DOING"
    TEST_DONE = "TEST_DONE"
    CODE_REVIEW_DOING = "CODE_REVIEW_DOING"
    CODE_REVIEW_DONE = "CODE_REVIEW_DONE"
    STAGE = "STAGE"
