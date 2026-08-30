import {
  useState
} from "react";

import MessageBubble from
  "./MessageBubble";

import SuggestedQuestions from
  "./SuggestedQuestions";

import {
  askQuestion
} from "../services/api";


function ChatWindow() {

  const [messages, setMessages] =
    useState([]);

  const [input, setInput] =
    useState("");

  const [loading, setLoading] =
    useState(false);


  const handleSend =
    async (question = input) => {

      if (!question.trim()) {
        return;
      }

      setMessages(
        previous => [
          ...previous,

          {
            role: "user",
            message: question
          }
        ]
      );

      setInput("");

      setLoading(true);

      try {

        const result =
          await askQuestion(
            question
          );

        setMessages(
          previous => [
            ...previous,

            {
              role: "assistant",

              message:
                result.answer
            }
          ]
        );

      } catch (error) {

        setMessages(
          previous => [
            ...previous,

            {
              role: "assistant",

              message:
                "Sorry, I was unable to retrieve the business data."
            }
          ]
        );

      } finally {

        setLoading(false);

      }
    };


  return (

    <div className="chat-container">

      <div className="chat-header">

        <h1>
          Skylark BI Agent
        </h1>

        <p>
          Ask questions about
          sales, pipeline and
          operations.
        </p>

      </div>


      {messages.length === 0 && (

        <SuggestedQuestions
          onSelect={handleSend}
        />

      )}


      <div className="messages">

        {messages.map(
          (item, index) => (

            <MessageBubble
              key={index}

              role={item.role}

              message={
                item.message
              }
            />

          )
        )}


        {loading && (

          <div
            className="loading"
          >
            Analyzing monday.com data...
          </div>

        )}

      </div>


      <div className="input-area">

        <input

          value={input}

          placeholder={
            "Ask a business question..."
          }

          onChange={(event) =>
            setInput(
              event.target.value
            )
          }

          onKeyDown={(event) => {

            if (
              event.key === "Enter"
            ) {

              handleSend();

            }

          }}

        />


        <button
          onClick={() =>
            handleSend()
          }
        >
          Send
        </button>

      </div>

    </div>

  );
}


export default ChatWindow;