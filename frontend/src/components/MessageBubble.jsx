import ReactMarkdown from 'react-markdown';

function MessageBubble({
  message,
  role
}) {

  return (
    <div
      className={`message ${role}`}
    >
      <ReactMarkdown>{message}</ReactMarkdown>
    </div>
  );
}

export default MessageBubble;