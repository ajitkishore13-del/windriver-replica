import React, { useEffect, useState } from 'react';
import { Header, Icon, Segment, Grid, Card, Statistic, Table, Label } from 'semantic-ui-react';
import { endpoints } from '../api/endpoints';

export default function SystemHealthPage() {
  const [clusterStatus, setClusterStatus] = useState<any>(null);
  const [nodes, setNodes] = useState<any[]>([]);

  useEffect(() => {
    endpoints.cluster.status().then((res) => setClusterStatus(res.data));
    endpoints.cluster.nodes().then((res) => setNodes(res.data.items));
  }, []);

  return (
    <div>
      <Header as="h2"><Icon name="heartbeat" /><Header.Content>System Health<Header.Subheader>Cluster and service status</Header.Subheader></Header.Content></Header>

      <Grid columns={2}>
        <Grid.Column>
          <Segment>
            <Header as="h4">Cluster Status</Header>
            <Card fluid>
              <Card.Content textAlign="center">
                <Statistic size="small" color={clusterStatus?.status === 'OK' ? 'green' : 'red'}>
                  <Statistic.Value><Icon name={clusterStatus?.status === 'OK' ? 'check circle' : 'exclamation circle'} />{clusterStatus?.status || 'Loading...'}</Statistic.Value>
                  <Statistic.Label>Overall Status</Statistic.Label>
                </Statistic>
              </Card.Content>
            </Card>
          </Segment>
        </Grid.Column>
        <Grid.Column>
          <Segment>
            <Header as="h4">Service Status</Header>
            {clusterStatus?.services && Object.entries(clusterStatus.services).map(([service, info]: any) => (
              <div key={service} style={{ marginBottom: '0.5em' }}>
                <strong>{service}:</strong>{' '}
                <Label size="tiny" color={info.status === 'OK' ? 'green' : 'red'}>{info.status}</Label>
              </div>
            ))}
          </Segment>
        </Grid.Column>
      </Grid>

      <Segment style={{ marginTop: '1em' }}>
        <Header as="h4">Cluster Nodes</Header>
        <Table celled striped>
          <Table.Header>
            <Table.Row>
              <Table.HeaderCell>Hostname</Table.HeaderCell>
              <Table.HeaderCell>Private IP</Table.HeaderCell>
              <Table.HeaderCell>Public IP</Table.HeaderCell>
              <Table.HeaderCell>Version</Table.HeaderCell>
              <Table.HeaderCell>Edition</Table.HeaderCell>
            </Table.Row>
          </Table.Header>
          <Table.Body>
            {nodes.map((n: any) => (
              <Table.Row key={n.id || n.hostname}>
                <Table.Cell><strong>{n.hostname}</strong></Table.Cell>
                <Table.Cell>{n.private_ip}</Table.Cell>
                <Table.Cell>{n.public_ip}</Table.Cell>
                <Table.Cell>{n.version}</Table.Cell>
                <Table.Cell>{n.edition}</Table.Cell>
              </Table.Row>
            ))}
          </Table.Body>
        </Table>
      </Segment>
    </div>
  );
}
