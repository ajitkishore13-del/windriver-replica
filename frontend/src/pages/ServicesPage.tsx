import React, { useEffect, useState } from 'react';
import { Table, Header, Icon, Button, Segment, Label } from 'semantic-ui-react';
import { endpoints } from '../api/endpoints';

export default function ServicesPage() {
  const [deployments, setDeployments] = useState<any[]>([]);

  const load = () => {
    endpoints.deployments.list().then((res) => {
      setDeployments(res.data.items.filter((d: any) => d.labels && d.labels.some((l: any) => l.env === 'production')));
    });
  };

  useEffect(() => { load(); }, []);

  return (
    <div>
      <Header as="h2">
        <Icon name="server" />
        <Header.Content>
          Services
          <Header.Subheader>Deployment services management</Header.Subheader>
        </Header.Content>
      </Header>

      <Segment>
        <div style={{ marginBottom: '1em' }}>
          <Button icon labelPosition="left" onClick={load}><Icon name="refresh" /> Refresh</Button>
        </div>
        <Table celled striped>
          <Table.Header>
            <Table.Row>
              <Table.HeaderCell>Service ID</Table.HeaderCell>
              <Table.HeaderCell>Blueprint</Table.HeaderCell>
              <Table.HeaderCell>Status</Table.HeaderCell>
              <Table.HeaderCell>Labels</Table.HeaderCell>
              <Table.HeaderCell>Outputs</Table.HeaderCell>
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
                <Table.Cell>
                  {(d.labels || []).map((l: any, i: number) => (
                    <Label key={i} size="mini">
                      {typeof l === 'string' ? l : Object.entries(l).map(([k, v]) => `${k}=${v}`).join(', ')}
                    </Label>
                  ))}
                </Table.Cell>
                <Table.Cell style={{ maxWidth: 200, overflow: 'hidden', textOverflow: 'ellipsis' }}>
                  {JSON.stringify(d.outputs || {})}
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
