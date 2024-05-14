import React, { useState } from 'react';
import { Container, Box, TextField, IconButton, Paper, Avatar, Typography, AppBar, Toolbar, Badge, CircularProgress } from '@mui/material';
import { Send, PhotoCamera, Cancel } from '@mui/icons-material';
import axios from 'axios';
import './chatbot.css';

function Chatbot() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [image, setImage] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSend = async () => {
    if (input.trim() || image) {
      const newMessage = { text: input, image, isUser: true };
      setMessages([...messages, newMessage]);
      setInput('');
      setImage(null);
      setLoading(true);

      try {
        const formData = new FormData();
        formData.append('message', input);
        if (image) {
          const blob = await fetch(image).then(res => res.blob());
          formData.append('image', blob);
        }

        const response = await axios.post('http://localhost:5000/chat', formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        });

        setMessages(prevMessages => [...prevMessages, { text: response.data.response, isUser: false }]);
      } catch (error) {
        console.error('Error sending message:', error);
      } finally {
        setLoading(false);
        
      }
    }
  };

  const handleImageUpload = (event) => {
    if (event.target.files[0]) {
      const reader = new FileReader();
      reader.onload = () => {
        setImage(reader.result);
      };
      reader.readAsDataURL(event.target.files[0]);
    }
  };

  const handleRemoveImage = () => {
    setImage(null);
  };

  return (
    <Container maxWidth="md" className="chat-container">
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6">Medy</Typography>
        </Toolbar>
      </AppBar>
      <Paper elevation={3} className="chat-box">
        <Box className="messages">
          {messages.map((msg, index) => (
            <Box
              key={index}
              className={`message ${msg.isUser ? 'user-message' : 'ai-message'}`}
              style={{ alignSelf: msg.isUser ? 'flex-end' : 'flex-start' }}
            >
              <Avatar className="avatar">{msg.isUser ? 'U' : 'M'}</Avatar>
              <Box className="message-content">
                {msg.text && <Typography variant="body1">{msg.text}</Typography>}
                {msg.image && <img src={msg.image} alt="uploaded" className="uploaded-image" />}
              </Box>
            </Box>
          ))}
          {loading && (
            <Box className="message ai-message" style={{ alignSelf: 'flex-start' }}>
              <Avatar className="avatar">AI</Avatar>
              <Box className="message-content">
                <CircularProgress size={24} />
              </Box>
            </Box>
          )}
        </Box>
        <Box className="input-box">
          <TextField
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Type a message"
            variant="outlined"
            fullWidth
            onKeyPress={(e) => e.key === 'Enter' && handleSend()}
            style={{ marginRight: '8px' }}
          />
          <input
            accept="image/*"
            style={{ display: 'none' }}
            id="icon-button-file"
            type="file"
            onChange={handleImageUpload}
          />
          <label htmlFor="icon-button-file">
            <IconButton color="primary" aria-label="upload picture" component="span">
              <PhotoCamera />
            </IconButton>
          </label>
          {image && (
            <Box className="image-preview">
              <Badge
                badgeContent={
                  <IconButton size="small" onClick={handleRemoveImage}>
                    <Cancel fontSize="small" />
                  </IconButton>
                }
              >
                <img src={image} alt="preview" className="preview-image" />
              </Badge>
            </Box>
          )}
          <IconButton color="primary" aria-label="send message" onClick={handleSend}>
            <Send />
          </IconButton>
        </Box>
      </Paper>
    </Container>
  );
}

export default Chatbot;
