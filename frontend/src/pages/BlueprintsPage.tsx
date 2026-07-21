import React, { useEffect, useState } from 'react';
import { Table, Button, Header, Icon, Modal, Form, Label, Segment, Input } from 'semantic-ui-react';
import { endpoints } from '../api/endpoints';

export default function BlueprintsPage() {
  const [blueprints, setBlueprints] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [showCreate, setShowCreate] = useState(false);
  const [newBp, setNewBp] = useState({ id: '', description: '', main_file_name: 'blueprint.yaml' });
  const [showDeploy, setShowDeploy] = useState(false);
  const [deployTarget, setDeployTarget] = useState('');
  const [newDepId, setNewDepId] = useState('');

  const load = () => {
    setLoading(true);
    endpoints.blueprints.list().then((res) => {
      setBlueprints(res.data.items);
    }).finally(() => setLoading(false));
  };

  useEffect(() => { load(); }, []);

  const handleCreate = async () => {
    await endpoints.blueprints.create(newBp.id, newBp);
    setShowCreate(false);
    setNewBp({ id: '', description: '', main_file_name: 'blueprint.yaml' });
    load();
  };

  const handleDeploy = async () => {
    await endpoints.deployments.create(newDepId, { id: newDepId, blueprint_id: deployTarget, display_name: newDepId });
    setShowDeploy(false);
    setNewDepId('');
    load();
  };

  const handleDelete = async (id: string) => {
    if (window.confirm(`Delete blueprint "${id}"?`)) {
      await endpoints.blueprints.delete(id);
      load();
    }
  };

  return (
    <div>
      <Header as="h2">
        <Icon name="file code outline" />
        <Header.Content>
          Blueprints
          <Header.Subheader>Manage infrastructure and application blueprints</Header.Subheader>
        </Header.Content>
      </Header>

      <Segment>
        <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '1em' }}>
          <Button primary icon labelPosition="left" onClick={() => setShowCreate(true)}>
            <Icon name="upload" /> Upload Blueprint
          </Button>
          <Button icon labelPosition="left" onClick={load}>
            <Icon name="refresh" /> Refresh
          </Button>
        </div>
        <Table celled striped>
          <Table.Header>
            <Table.Row>
              <Table.HeaderCell>ID</Table.HeaderCell>
              <Table.HeaderCell>Description</Table.HeaderCell>
              <Table.HeaderCell>Created By</Table.HeaderCell>
              <Table.HeaderCell>Visibility</Table.HeaderCell>
              <Table.HeaderCell>Labels</Table.HeaderCell>
              <Table.HeaderCell>Created</Table.HeaderCell>
              <Table.HeaderCell>Actions</Table.HeaderCell>
            </Table.Row>
          </Table.Header>
          <Table.Body>
            {loading && (
              <Table.Row>
                <Table.Cell colSpan={7} textAlign="center">Loading...</Table.Cell>
              </Table.Row>
            )}
            {!loading && blueprints.length === 0 && (
              <Table.Row>
                <Table.Cell colSpan={7} textAlign="center">No blueprints found. Upload one to get started.</Table.Cell>
              </Table.Row>
            )}
            {blueprints.map((bp: any) => (
              <Table.Row key={bp.id}>
                <Table.Cell><strong>{bp.id}</strong></Table.Cell>
                <Table.Cell>{bp.description}</Table.Cell>
                <Table.Cell>{bp.created_by}</Table.Cell>
                <Table.Cell>
                  <Label size="tiny" color={bp.visibility === 'global' ? 'green' : 'grey'}>
                    {bp.visibility}
                  </Label>
                </Table.Cell>
                <Table.Cell>
                  {(bp.labels || []).map((l: any, i: number) => (
                    <Label key={i} size="mini">
                      {typeof l === 'string' ? l : Object.entries(l).map(([k, v]) => `${k}=${v}`).join(', ')}
                    </Label>
                  ))}
                </Table.Cell>
                <Table.Cell>{bp.created_at ? new Date(bp.created_at).toLocaleDateString() : '-'}</Table.Cell>
                <Table.Cell>
                  <Button size="mini" color="green" icon="rocket"
                    onClick={() => { setDeployTarget(bp.id); setNewDepId(`${bp.id}-dep`); setShowDeploy(true); }}
                    title="Create Deployment"
                  />
                  <Button size="mini" color="red" icon="trash"
                    onClick={() => handleDelete(bp.id)}
                    title="Delete"
                  />
                </Table.Cell>
              </Table.Row>
            ))}
          </Table.Body>
        </Table>
      </Segment>

      <Modal open={showCreate} onClose={() => setShowCreate(false)} size="small">
        <Modal.Header>Upload Blueprint</Modal.Header>
        <Modal.Content>
          <Form>
            <Form.Input label="Blueprint ID" value={newBp.id} onChange={(e) => setNewBp({ ...newBp, id: e.target.value })} />
            <Form.TextArea label="Description" value={newBp.description} onChange={(e) => setNewBp({ ...newBp, description: e.target.value })} />
            <Form.Input label="Main File Name" value={newBp.main_file_name} onChange={(e) => setNewBp({ ...newBp, main_file_name: e.target.value })} />
          </Form>
        </Modal.Content>
        <Modal.Actions>
          <Button onClick={() => setShowCreate(false)}>Cancel</Button>
          <Button primary onClick={handleCreate} disabled={!newBp.id}>Upload</Button>
        </Modal.Actions>
      </Modal>

      <Modal open={showDeploy} onClose={() => setShowDeploy(false)} size="small">
        <Modal.Header>Create Deployment from "{deployTarget}"</Modal.Header>
        <Modal.Content>
          <Form>
            <Form.Input label="Deployment ID" value={newDepId} onChange={(e) => setNewDepId(e.target.value)} />
          </Form>
        </Modal.Content>
        <Modal.Actions>
          <Button onClick={() => setShowDeploy(false)}>Cancel</Button>
          <Button primary onClick={handleDeploy} disabled={!newDepId}>Create Deployment</Button>
        </Modal.Actions>
      </Modal>
    </div>
  );
}
