function MessageBubble({
  message,
  role
}) {

  return (
    <div
      className={`message ${role}`}
    >
      {message}
    </div>
  );
}

export default MessageBubble;