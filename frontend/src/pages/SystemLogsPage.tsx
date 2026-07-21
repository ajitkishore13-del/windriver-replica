import React, { useEffect, useState } from 'react';
import { Table, Header, Icon, Button, Segment, Label, Dropdown } from 'semantic-ui-react';
import { endpoints } from '../api/endpoints';

export default function SystemLogsPage() {
  const [events, setEvents] = useState<any[]>([]);
  const [level, setLevel] = useState<string>('');

  const load = () => {
    const params: any = {};
    if (level) params.level = level;
    endpoints.events.list(params).then((res) => setEvents(res.data.items));
  };

  useEffect(() => { load(); }, [level]);

  return (
    <div>
      <Header as="h2"><Icon name="file text" /><Header.Content>System Logs<Header.Subheader>Events and log analysis</Header.Subheader></Header.Content></Header>
      <Segment>
        <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '1em' }}>
          <div>
            <Button icon labelPosition="left" onClick={load}><Icon name="refresh" /> Refresh</Button>
          </div>
          <div>
            <Dropdown
              selection clearable
              placeholder="Filter by level"
              options={[
                { text: 'All', value: '' },
                { text: 'Info', value: 'info' },
                { text: 'Error', value: 'error' },
                { text: 'Warning', value: 'warning' },
              ]}
              value={level}
              onChange={(e, d) => setLevel(d.value as string)}
            />
          </div>
        </div>
        <Table celled striped>
          <Table.Header>
            <Table.Row>
              <Table.HeaderCell>Timestamp</Table.HeaderCell>
              <Table.HeaderCell>Level</Table.HeaderCell>
              <Table.HeaderCell>Event Type</Table.HeaderCell>
              <Table.HeaderCell>Message</Table.HeaderCell>
              <Table.HeaderCell>Execution</Table.HeaderCell>
              <Table.HeaderCell>Deployment</Table.HeaderCell>
            </Table.Row>
          </Table.Header>
          <Table.Body>
            {events.map((e: any) => (
              <Table.Row key={e.id}>
                <Table.Cell>{e.timestamp ? new Date(e.timestamp).toLocaleString() : '-'}</Table.Cell>
                <Table.Cell>
                  <Label size="mini" color={e.level === 'error' ? 'red' : e.level === 'warning' ? 'yellow' : 'blue'}>
                    {e.level}
                  </Label>
                </Table.Cell>
                <Table.Cell>{e.event_type}</Table.Cell>
                <Table.Cell style={{ maxWidth: 300 }}>{e.message}</Table.Cell>
                <Table.Cell>{e.execution_id || '-'}</Table.Cell>
                <Table.Cell>{e.deployment_id || '-'}</Table.Cell>
              </Table.Row>
            ))}
          </Table.Body>
        </Table>
      </Segment>
    </div>
  );
}
