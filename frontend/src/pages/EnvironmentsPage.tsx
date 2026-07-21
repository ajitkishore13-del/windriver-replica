import React, { useEffect, useState } from 'react';
import { Table, Header, Icon, Button, Segment, Label } from 'semantic-ui-react';
import { endpoints } from '../api/endpoints';

export default function EnvironmentsPage() {
  const [deployments, setDeployments] = useState<any[]>([]);

  const load = () => {
    endpoints.deployments.list().then((res) => {
      setDeployments(res.data.items.filter((d: any) => !d.labels || d.labels.length === 0 || d.labels.some((l: any) => l.env === 'staging')));
    });
  };

  useEffect(() => { load(); }, []);

  return (
    <div>
      <Header as="h2">
        <Icon name="cubes" />
        <Header.Content>
          Environments
          <Header.Subheader>Deployment environments management</Header.Subheader>
        </Header.Content>
      </Header>

      <Segment>
        <div style={{ marginBottom: '1em' }}>
          <Button icon labelPosition="left" onClick={load}><Icon name="refresh" /> Refresh</Button>
        </div>
        <Table celled striped>
          <Table.Header>
            <Table.Row>
              <Table.HeaderCell>Environment ID</Table.HeaderCell>
              <Table.HeaderCell>Blueprint</Table.HeaderCell>
              <Table.HeaderCell>Status</Table.HeaderCell>
              <Table.HeaderCell>Site</Table.HeaderCell>
              <Table.HeaderCell>Capabilities</Table.HeaderCell>
              <Table.HeaderCell>Created</Table.HeaderCell>
            </Table.Row>
          </Table.Header>
          <Table.Body>
            {deployments.map((d: any) => (
              <Table.Row key={d.id}>
                <Table.Cell><strong>{d.id}</strong></Table.Cell>
                <Table.Cell>{d.blueprint_id}</Table.Cell>
                <Table.Cell>
                  <Label size="tiny" color={d.status === 'active' ? 'green' : 'red'}>{d.status}</Label>
                </Table.Cell>
                <Table.Cell>{d.site_name || '-'}</Table.Cell>
                <Table.Cell style={{ maxWidth: 200, overflow: 'hidden', textOverflow: 'ellipsis' }}>
                  {JSON.stringify(d.capabilities || {})}
                </Table.Cell>
                <Table.Cell>{d.created_at ? new Date(d.created_at).toLocaleDateString() : '-'}</Table.Cell>
              </Table.Row>
            ))}
          </Table.Body>
        </Table>
      </Segment>
    </div>
  );
}
