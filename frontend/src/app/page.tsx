'use client';

import React, { useState } from "react";
import { TextField, IconButton, Box, Typography } from "@mui/material";
import SendIcon from "@mui/icons-material/Send";
import AttachFileIcon from "@mui/icons-material/AttachFile";
import CloseIcon from "@mui/icons-material/Close";
import PictureAsPdfIcon from "@mui/icons-material/PictureAsPdf";
import ImageIcon from "@mui/icons-material/Image";
import DescriptionIcon from "@mui/icons-material/Description";
import InsertDriveFileIcon from "@mui/icons-material/InsertDriveFile";

const Chat = () => {
  const [messages, setMessages] = useState<{ sender: string; text: string }[]>([]);
  const [input, setInput] = useState("");
  const [file, setFile] = useState<File | null>(null);

  const handleSend = () => {
    if (input.trim()) {
      setMessages([...messages, { sender: "User", text: input }]);
      setInput("");
      setTimeout(() => {
        setMessages((prev) => [...prev, { sender: "ChatGPT", text: "This is a response!" }]);
      }, 1000);
    }
  };

  const handleFileUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const uploadedFile = event.target.files?.[0] || null;
    setFile(uploadedFile);
  };

  const handleFileRemove = () => {
    setFile(null);
  };

  const getFileIcon = (fileName: string) => {
    const extension = fileName.split(".").pop()?.toLowerCase();
    switch (extension) {
      case "pdf":
        return <PictureAsPdfIcon fontSize="small" sx={{ color: "red", mr: 1 }} />;
      case "jpg":
      case "jpeg":
      case "png":
      case "gif":
        return <ImageIcon fontSize="small" sx={{ color: "blue", mr: 1 }} />;
      case "doc":
      case "docx":
      case "txt":
        return <DescriptionIcon fontSize="small" sx={{ color: "green", mr: 1 }} />;
      default:
        return <InsertDriveFileIcon fontSize="small" sx={{ color: "gray", mr: 1 }} />;
    }
  };

  return (
    <Box className="flex flex-col h-screen bg-gradient-to-b from-gray-800 items-center gap-10">
      
      {/* Messages Area */}
      <Box className="flex-1 overflow-y-auto p-4 w-full md:w-3/4 lg:w-1/2">
        {messages.map((msg, index) => (
          <div
            key={index}
            className={`flex ${
              msg.sender === "User" ? "justify-end" : "justify-start"
            } mb-2`}
          >
            <div
              className={`max-w-sm p-3 rounded-lg ${
                msg.sender === "User"
                  ? "bg-black text-white"
                  : "bg-gray-700 text-white"
              }`}
            >
              {msg.text}
            </div>
          </div>
        ))}
      </Box>

      <Box className="w-4/5 md:w-3/4 lg:w-1/2 mb-5">
        {file && (
          <Box className="mb-2 p-2 bg-green-400 rounded-lg flex items-center justify-between">
            <Box
              className="flex items-center overflow-hidden"
              sx={{ flexGrow: 1, minWidth: 0 }}
            >
              {getFileIcon(file.name)}
              <Typography
                variant="body2"
                sx={{
                  color: "black",
                  whiteSpace: "nowrap",
                  overflow: "hidden",
                  textOverflow: "ellipsis",
                  ml: 1,
                }}
                title={file.name}
              >
                {file.name}
              </Typography>
            </Box>
            <IconButton size="small" onClick={handleFileRemove}>
              <CloseIcon fontSize="small" />
            </IconButton>
          </Box>
        )}

    
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

          <IconButton color="inherit" onClick={handleSend}>
            <SendIcon />
          </IconButton>
        </Box>
      </Box>
    </Box>
  );
};

export default Chat;
