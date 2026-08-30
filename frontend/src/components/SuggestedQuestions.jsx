function SuggestedQuestions({
  onSelect
}) {

  const questions = [

    "How is our pipeline looking overall?",

    "How is the Energy sector pipeline this quarter?",

    "What is the work order completion rate?",

    "Compare pipeline and work order performance by sector.",

    "Prepare a leadership update."
  ];

  return (

    <div className="suggestions">

      <h3>
        Try asking
      </h3>

      {questions.map(
        (question) => (

          <button
            key={question}

            onClick={() =>
              onSelect(question)
            }
          >
            {question}
          </button>

        )
      )}

    </div>

  );
}

export default SuggestedQuestions;