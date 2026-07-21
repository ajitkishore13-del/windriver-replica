import React, { useEffect, useState } from 'react';
import { Grid, Card, Header, Icon, Segment, Image, Label, Button } from 'semantic-ui-react';
import { endpoints } from '../api/endpoints';

export default function CatalogPage() {
  const [blueprints, setBlueprints] = useState<any[]>([]);
  const [plugins, setPlugins] = useState<any[]>([]);

  useEffect(() => {
    endpoints.blueprints.list().then((res) => setBlueprints(res.data.items));
    endpoints.plugins.list().then((res) => setPlugins(res.data.items));
  }, []);

  return (
    <div>
      <Header as="h2">
        <Icon name="shopping cart" />
        <Header.Content>
          Catalog
          <Header.Subheader>Blueprint examples and plugins marketplace</Header.Subheader>
        </Header.Content>
      </Header>

      <Grid columns={2} divided>
        <Grid.Row>
          <Grid.Column>
            <Segment>
              <Header as="h4"><Icon name="file code outline" /> Blueprints Catalog</Header>
              <Card.Group itemsPerRow={2}>
                {blueprints.map((bp: any) => (
                  <Card key={bp.id} fluid>
                    <Card.Content>
                      <Card.Header>{bp.id}</Card.Header>
                      <Card.Meta style={{ fontSize: '0.85em', color: '#888' }}>{bp.main_file_name}</Card.Meta>
                      <Card.Description style={{ fontSize: '0.85em' }}>
                        {bp.description || 'No description'}
                      </Card.Description>
                    </Card.Content>
                    <Card.Content extra>
                      <Label size="tiny">{bp.visibility}</Label>
                      <span style={{ float: 'right', fontSize: '0.8em', color: '#888' }}>by {bp.created_by}</span>
                    </Card.Content>
                  </Card>
                ))}
              </Card.Group>
            </Segment>
          </Grid.Column>
          <Grid.Column>
            <Segment>
              <Header as="h4"><Icon name="puzzle piece" /> Plugins Catalog</Header>
              <Card.Group itemsPerRow={2}>
                {plugins.map((p: any) => (
                  <Card key={p.id} fluid>
                    <Card.Content>
                      <Card.Header>{p.package_name}</Card.Header>
                      <Card.Meta style={{ fontSize: '0.85em', color: '#888' }}>v{p.package_version}</Card.Meta>
                      <Card.Description style={{ fontSize: '0.85em' }}>
                        Platform: {p.supported_platform}
                      </Card.Description>
                    </Card.Content>
                    <Card.Content extra>
                      <Label size="tiny">{p.visibility}</Label>
                    </Card.Content>
                  </Card>
                ))}
              </Card.Group>
            </Segment>
          </Grid.Column>
        </Grid.Row>
      </Grid>
    </div>
  );
}
