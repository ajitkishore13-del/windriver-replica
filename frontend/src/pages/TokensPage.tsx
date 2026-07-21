import React, { useState } from 'react';
import { Header, Icon, Button, Segment, Form, Message } from 'semantic-ui-react';
import { endpoints } from '../api/endpoints';

export default function TokensPage() {
  const [token, setToken] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const generateToken = async () => {
    setLoading(true);
    try {
      const res = await endpoints.tokens();
      setToken(res.data.value);
    } catch (e) {
      console.error(e);
    }
    setLoading(false);
  };

  return (
    <div>
      <Header as="h2"><Icon name="key" /><Header.Content>Tokens<Header.Subheader>Authentication tokens</Header.Subheader></Header.Content></Header>
      <Segment>
        <p>Generate authentication tokens for API access. Tokens can be used instead of username/password for Basic Auth.</p>
        <Button primary icon labelPosition="left" loading={loading} onClick={generateToken}>
          <Icon name="key" /> Generate Token
        </Button>
        {token && (
          <Message positive style={{ marginTop: '1em' }}>
            <Message.Header>Token Generated</Message.Header>
            <pre style={{ wordBreak: 'break-all', whiteSpace: 'pre-wrap' }}>{token}</pre>
          </Message>
        )}
      </Segment>
    </div>
  );
}
