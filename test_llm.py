from agent.llm_router import detect_intent

print(
    detect_intent(
        "Which columns have missing values?"
    )
)

print(
    detect_intent(
        "Is this dataset ready for machine learning?"
    )
)

print(
    detect_intent(
        "What preprocessing do you recommend?"
    )
)