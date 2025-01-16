'use client';

import React from "react";
import { Box, Typography, IconButton } from "@mui/material";
import CloseIcon from "@mui/icons-material/Close";
import PictureAsPdfIcon from "@mui/icons-material/PictureAsPdf";
import ImageIcon from "@mui/icons-material/Image";
import DescriptionIcon from "@mui/icons-material/Description";
import InsertDriveFileIcon from "@mui/icons-material/InsertDriveFile";

interface AttachmentProps {
  file: File | null;
  onRemove?: () => void;
}

const Attachment: React.FC<AttachmentProps> = ({ file, onRemove }) => {
  if (!file) return null;

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
    <Box className="mb-2 p-2 bg-green-400 rounded-lg flex items-center justify-between">
      <Box className="flex items-center overflow-hidden" sx={{ flexGrow: 1, minWidth: 0 }}>
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
      {
        onRemove &&
        <IconButton size="small" onClick={onRemove}>
          <CloseIcon fontSize="small" />
        </IconButton>
      }
      
    </Box>
  );
};

export default Attachment;