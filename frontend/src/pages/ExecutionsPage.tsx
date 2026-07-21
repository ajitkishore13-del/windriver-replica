import React, { useEffect, useState } from 'react';
import { Table, Header, Icon, Button, Segment, Label, Grid, Card, Statistic } from 'semantic-ui-react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { endpoints } from '../api/endpoints';

export default function ExecutionsPage() {
  const [executions, setExecutions] = useState<any[]>([]);

  const load = () => {
    endpoints.executions.list().then((res) => setExecutions(res.data.items));
  };

  useEffect(() => { load(); }, []);

  const statusCounts = executions.reduce((acc: any, e: any) => {
    acc[e.status] = (acc[e.status] || 0) + 1;
    return acc;
  }, {} as Record<string, number>);

  const chartData = Object.entries(statusCounts).map(([name, value]) => ({ name, value }));

  const statusColor = (s: string) => {
    const map: Record<string, string> = { started: 'yellow', succeeded: 'green', failed: 'red', cancelled: 'grey', pending: 'blue' };
    return map[s] || 'grey';
  };

  return (
    <div>
      <Header as="h2">
        <Icon name="play circle" />
        <Header.Content>
          Executions
          <Header.Subheader>Workflow execution monitoring</Header.Subheader>
        </Header.Content>
      </Header>

      <Grid columns={2} style={{ marginBottom: '1em' }}>
        <Grid.Column>
          <Card.Group itemsPerRow={5}>
            {Object.entries(statusCounts).map(([status, count]) => (
              <Card key={status}>
                <Card.Content textAlign="center">
                  <Statistic size="tiny" color={statusColor(status) as any}>
                    <Statistic.Value>{count as number}</Statistic.Value>
                    <Statistic.Label>{status}</Statistic.Label>
                  </Statistic>
                </Card.Content>
              </Card>
            ))}
          </Card.Group>
        </Grid.Column>
        <Grid.Column>
          <Segment>
            <ResponsiveContainer width="100%" height={120}>
              <BarChart data={chartData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis allowDecimals={false} />
                <Tooltip />
                <Bar dataKey="value" fill="#00b5ad" />
              </BarChart>
            </ResponsiveContainer>
          </Segment>
        </Grid.Column>
      </Grid>

      <Segment>
        <div style={{ marginBottom: '1em' }}>
          <Button icon labelPosition="left" onClick={load}><Icon name="refresh" /> Refresh</Button>
        </div>
        <Table celled striped>
          <Table.Header>
            <Table.Row>
              <Table.HeaderCell>Execution ID</Table.HeaderCell>
              <Table.HeaderCell>Deployment</Table.HeaderCell>
              <Table.HeaderCell>Workflow</Table.HeaderCell>
              <Table.HeaderCell>Status</Table.HeaderCell>
              <Table.HeaderCell>Started</Table.HeaderCell>
              <Table.HeaderCell>Ended</Table.HeaderCell>
              <Table.HeaderCell>Error</Table.HeaderCell>
            </Table.Row>
          </Table.Header>
          <Table.Body>
            {executions.map((e: any) => (
              <Table.Row key={e.id}>
                <Table.Cell><strong>{e.id}</strong></Table.Cell>
                <Table.Cell>{e.deployment_id}</Table.Cell>
                <Table.Cell>{e.workflow_id}</Table.Cell>
                <Table.Cell>
                  <Label size="tiny" color={statusColor(e.status) as any}>{e.status}</Label>
                </Table.Cell>
                <Table.Cell>{e.started_at ? new Date(e.started_at).toLocaleString() : '-'}</Table.Cell>
                <Table.Cell>{e.ended_at ? new Date(e.ended_at).toLocaleString() : '-'}</Table.Cell>
                <Table.Cell style={{ color: 'red' }}>{e.error || '-'}</Table.Cell>
              </Table.Row>
            ))}
          </Table.Body>
        </Table>
      </Segment>
    </div>
  );
}
