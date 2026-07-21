import React, { useEffect, useState } from 'react';
import { Table, Header, Icon, Button, Segment } from 'semantic-ui-react';
import { endpoints } from '../api/endpoints';

export default function AgentsPage() {
  const [agents, setAgents] = useState<any[]>([]);

  const load = () => endpoints.agents.list().then((res) => setAgents(res.data.items));

  useEffect(() => { load(); }, []);

  return (
    <div>
      <Header as="h2"><Icon name="microchip" /><Header.Content>Agents<Header.Subheader>Installed Conductor agents</Header.Subheader></Header.Content></Header>
      <Segment>
        <div style={{ marginBottom: '1em' }}>
          <Button icon labelPosition="left" onClick={load}><Icon name="refresh" /> Refresh</Button>
        </div>
        <Table celled striped>
          <Table.Header>
            <Table.Row>
              <Table.HeaderCell>Agent ID</Table.HeaderCell>
              <Table.HeaderCell>IP</Table.HeaderCell>
              <Table.HeaderCell>System</Table.HeaderCell>
              <Table.HeaderCell>Version</Table.HeaderCell>
              <Table.HeaderCell>Install Method</Table.HeaderCell>
              <Table.HeaderCell>Node</Table.HeaderCell>
              <Table.HeaderCell>Deployment</Table.HeaderCell>
            </Table.Row>
          </Table.Header>
          <Table.Body>
            {agents.map((a: any) => (
              <Table.Row key={a.id}>
                <Table.Cell><strong>{a.id}</strong></Table.Cell>
                <Table.Cell>{a.ip}</Table.Cell>
                <Table.Cell>{a.system}</Table.Cell>
                <Table.Cell>{a.version}</Table.Cell>
                <Table.Cell>{a.install_method}</Table.Cell>
                <Table.Cell>{a.node}</Table.Cell>
                <Table.Cell>{a.deployment || '-'}</Table.Cell>
              </Table.Row>
            ))}
          </Table.Body>
        </Table>
      </Segment>
    </div>
  );
}
