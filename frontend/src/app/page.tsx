'use client';

import React, { useState } from "react";
import { TextField, IconButton, Box, Typography, CircularProgress } from "@mui/material";
import SendIcon from "@mui/icons-material/Send";
import AttachFileIcon from "@mui/icons-material/AttachFile";
import Attachment from "./components/Attachment";

const Chat = () => {
  const [messages, setMessages] = useState<{ sender: string; text: string, file?: File | null }[]>([]);
  const [input, setInput] = useState("");
  const [file, setFile] = useState<File | null>(null);
  const [isStreaming, setIsStreaming] = useState(false);

  const handleSend = async () => {
    if (input.trim() || file) {
      // Add user message to the chat
      setMessages([...messages, { sender: "User", text: input, file: file }]);
      setInput("");
      setFile(null);
      setIsStreaming(true);
  
      const formData = new FormData();
      formData.append("query", input);
      if (file) {
        formData.append("file", file);
      }
  
      try {
        const response = await fetch("http://127.0.0.1:5000/query", {
          method: "POST",
          body: formData,
        });
  
        if (!response.body) {
          throw new Error("No response body");
        }
  
        const reader = response.body.getReader();
        const decoder = new TextDecoder("utf-8");
        let partialMessage = "";
  
        // Add initial placeholder for streaming response
        setMessages((prev) => [...prev, { sender: "ChatGPT", text: "" }]);
  
        while (true) {
          const { done, value } = await reader.read();
          if (done) break;
  
          // Decode the chunk and append it to the partial message
          partialMessage += decoder.decode(value, { stream: true });
  
          // Update the last message in the chat
          setMessages((prev) => {
            const updatedMessages = [...prev];
            updatedMessages[updatedMessages.length - 1] = {
              sender: "ChatGPT",
              text: partialMessage,
            };
            return updatedMessages;
          });
        }
  
        setIsStreaming(false); // Mark streaming as completed
      } catch (error) {
        console.error("Error streaming response:", error);
        setMessages((prev) => [
          ...prev,
          { sender: "ChatGPT", text: "Failed to fetch response." },
        ]);
        setIsStreaming(false);
      } finally {
        setFile(null); // Clear file after sending
      }
    }
  };

  const handleFileUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const uploadedFile = event.target.files?.[0] || null;
    setFile(uploadedFile);
  };

  const handleFileRemove = () => {
    setFile(null);
  };

  return (
    <Box className="flex flex-col h-screen bg-gradient-to-b from-gray-800 items-center gap-10">
      
      {/* Messages Area */}
      <Box className="flex-1 overflow-y-auto w-full md:w-3/4 lg:w-1/2">
        {messages.map((msg, index) => (
          <div
            key={index}
            className={`flex ${
              msg.sender === "User" ? "justify-end" : "justify-start"
            } mb-2`}
          >
            <div
              className={`max-w-sm p-3 rounded-lg flex gap-3 flex-col ${
                msg.sender === "User"
                  ? "bg-black text-white"
                  : "bg-gray-700 text-white"
              }`}
            >
              {msg.text}
              {msg.file && <Attachment file={msg.file}/>}
            </div>
          </div>
        ))}
      </Box>

      <Box className="w-4/5 md:w-3/4 lg:w-1/2 mb-5">
        {file && <Attachment file={file} onRemove={handleFileRemove} />}

    
        <Box className="bg-gray-700 flex items-center p-2 rounded-lg">
          <IconButton component="label" color="inherit" className="mr-2">
            <AttachFileIcon />
            <input type="file" hidden onChange={handleFileUpload} />
          </IconButton>

          <TextField
            variant="outlined"
            fullWidth
            size="medium"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Type a message..."
            multiline
            maxRows={4}
            sx={{
              "& .MuiOutlinedInput-root": {
                padding: "10px",
                "& fieldset": { borderColor: "transparent" },
                "&:hover fieldset": { borderColor: "transparent" },
                "&.Mui-focused fieldset": { borderColor: "transparent" },
              },
              textarea: {
                color: "white",
                overflow: "auto",
                "&::-webkit-scrollbar": {
                  width: "4px",
                },
                "&::-webkit-scrollbar-thumb": {
                  backgroundColor: "white",
                  borderRadius: "4px",
                },
                "&::-webkit-scrollbar-track": {
                  backgroundColor: "transparent",
                },
              },
            }}
          />

          <IconButton color="inherit" onClick={handleSend} disabled={isStreaming || !input}>
            {isStreaming ? (
              <CircularProgress size={24} sx={{ color: "white" }} />
            ) : (
              <SendIcon />
            )}
          </IconButton>
        </Box>
      </Box>
    </Box>
  );
};

export default Chat;
