import React, { useState } from 'react';
import { Container, Segment, Form, Button, Header, Icon, Message } from 'semantic-ui-react';
import { useNavigate } from 'react-router-dom';
import { setAuth, getAuth } from '../api/client';
import api from '../api/client';

export default function LoginPage() {
  const [username, setUsername] = useState('admin');
  const [password, setPassword] = useState('admin');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleLogin = async () => {
    setLoading(true);
    setError('');
    setAuth(username, password);
    try {
      await api.get('/status');
      navigate('/dashboard');
    } catch {
      setError('Invalid credentials. Try admin/admin.');
      localStorage.removeItem('windriver_auth');
    }
    setLoading(false);
  };

  return (
    <Container style={{ height: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
      <Segment padded style={{ width: 400 }}>
        <Header as="h2" textAlign="center" color="teal">
          <Icon name="cloud" />
          <Header.Content>
            Wind River Studio
            <Header.Subheader>Conductor Management Console</Header.Subheader>
          </Header.Content>
        </Header>
        <Form onSubmit={handleLogin} error={!!error}>
          <Form.Input
            label="Username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            icon="user"
            iconPosition="left"
          />
          <Form.Input
            label="Password"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            icon="lock"
            iconPosition="left"
          />
          {error && <Message error content={error} />}
          <Button primary fluid loading={loading} type="submit">
            Sign In
          </Button>
        </Form>
      </Segment>
    </Container>
  );
}
