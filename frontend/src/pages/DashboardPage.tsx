import React, { useEffect, useState } from 'react';
import { Grid, Card, Statistic, Header, Segment, Icon } from 'semantic-ui-react';
import { endpoints } from '../api/endpoints';

export default function DashboardPage() {
  const [stats, setStats] = useState<any>({});

  useEffect(() => {
    Promise.all([
      endpoints.status(),
      endpoints.blueprints.list(),
      endpoints.deployments.list(),
      endpoints.executions.list(),
      endpoints.secrets.list(),
      endpoints.plugins.list(),
      endpoints.cluster.status(),
    ]).then(([statusRes, bpRes, depRes, execRes, secRes, plgRes, clsRes]) => {
      setStats({
        status: statusRes.data.status,
        blueprints: bpRes.data.metadata.pagination.total,
        deployments: depRes.data.metadata.pagination.total,
        executions: execRes.data.metadata.pagination.total,
        secrets: secRes.data.metadata.pagination.total,
        plugins: plgRes.data.metadata.pagination.total,
        cluster: clsRes.data.status,
      });
    });
  }, []);

  return (
    <div>
      <Header as="h2">
        <Icon name="dashboard" />
        <Header.Content>
          Dashboard
          <Header.Subheader>Wind River Studio Conductor Management Console</Header.Subheader>
        </Header.Content>
      </Header>

      <Card.Group itemsPerRow={4} style={{ marginBottom: '2em' }}>
        <Card>
          <Card.Content textAlign="center">
            <Statistic size="tiny" color="teal">
              <Statistic.Value><Icon name="file code" />{stats.blueprints ?? '-'}</Statistic.Value>
              <Statistic.Label>Blueprints</Statistic.Label>
            </Statistic>
          </Card.Content>
        </Card>
        <Card>
          <Card.Content textAlign="center">
            <Statistic size="tiny" color="blue">
              <Statistic.Value><Icon name="server" />{stats.deployments ?? '-'}</Statistic.Value>
              <Statistic.Label>Deployments</Statistic.Label>
            </Statistic>
          </Card.Content>
        </Card>
        <Card>
          <Card.Content textAlign="center">
            <Statistic size="tiny" color="green">
              <Statistic.Value><Icon name="play circle" />{stats.executions ?? '-'}</Statistic.Value>
              <Statistic.Label>Executions</Statistic.Label>
            </Statistic>
          </Card.Content>
        </Card>
        <Card>
          <Card.Content textAlign="center">
            <Statistic size="tiny" color="purple">
              <Statistic.Value><Icon name="lock" />{stats.secrets ?? '-'}</Statistic.Value>
              <Statistic.Label>Secrets</Statistic.Label>
            </Statistic>
          </Card.Content>
        </Card>
        <Card>
          <Card.Content textAlign="center">
            <Statistic size="tiny" color="orange">
              <Statistic.Value><Icon name="puzzle piece" />{stats.plugins ?? '-'}</Statistic.Value>
              <Statistic.Label>Plugins</Statistic.Label>
            </Statistic>
          </Card.Content>
        </Card>
        <Card>
          <Card.Content textAlign="center">
            <Statistic size="tiny" color={stats.cluster === 'OK' ? 'green' : 'red'}>
              <Statistic.Value><Icon name="heartbeat" />{stats.cluster ?? '-'}</Statistic.Value>
              <Statistic.Label>Cluster Status</Statistic.Label>
            </Statistic>
          </Card.Content>
        </Card>
      </Card.Group>

      <Grid columns={2} divided>
        <Grid.Row>
          <Grid.Column>
            <Segment>
              <Header as="h4"><Icon name="file code outline" /> Recent Blueprints</Header>
              <p style={{ color: '#888', fontSize: '0.85em' }}>
                Use the Blueprints page to upload, manage, and deploy blueprints. Blueprints define the infrastructure and application topology.
              </p>
            </Segment>
          </Grid.Column>
          <Grid.Column>
            <Segment>
              <Header as="h4"><Icon name="play circle" /> Quick Actions</Header>
              <p style={{ color: '#888', fontSize: '0.85em' }}>
                Upload a new blueprint, create a deployment, or execute a workflow from the respective management pages.
              </p>
            </Segment>
          </Grid.Column>
        </Grid.Row>
      </Grid>
    </div>
  );
}
