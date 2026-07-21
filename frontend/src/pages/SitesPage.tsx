import React, { useEffect, useState } from 'react';
import { Table, Header, Icon, Button, Segment, Modal, Form } from 'semantic-ui-react';
import { endpoints } from '../api/endpoints';

export default function SitesPage() {
  const [sites, setSites] = useState<any[]>([]);
  const [showCreate, setShowCreate] = useState(false);
  const [newSite, setNewSite] = useState({ name: '', location: '' });

  const load = () => endpoints.sites.list().then((res) => setSites(res.data.items));

  useEffect(() => { load(); }, []);

  const handleCreate = async () => {
    await endpoints.sites.create(newSite.name, newSite);
    setShowCreate(false);
    setNewSite({ name: '', location: '' });
    load();
  };

  const handleDelete = async (name: string) => {
    if (window.confirm(`Delete site "${name}"?`)) {
      await endpoints.sites.delete(name);
      load();
    }
  };

  return (
    <div>
      <Header as="h2"><Icon name="map marker" /><Header.Content>Sites<Header.Subheader>Manage deployment sites</Header.Subheader></Header.Content></Header>
      <Segment>
        <div style={{ marginBottom: '1em' }}>
          <Button primary icon labelPosition="left" onClick={() => setShowCreate(true)}>
            <Icon name="plus" /> Create Site
          </Button>
        </div>
        <Table celled striped>
          <Table.Header>
            <Table.Row>
              <Table.HeaderCell>Name</Table.HeaderCell>
              <Table.HeaderCell>Location</Table.HeaderCell>
              <Table.HeaderCell>Tenant</Table.HeaderCell>
              <Table.HeaderCell>Created</Table.HeaderCell>
              <Table.HeaderCell>Actions</Table.HeaderCell>
            </Table.Row>
          </Table.Header>
          <Table.Body>
            {sites.map((s: any) => (
              <Table.Row key={s.name}>
                <Table.Cell><strong>{s.name}</strong></Table.Cell>
                <Table.Cell>{s.location}</Table.Cell>
                <Table.Cell>{s.tenant_name}</Table.Cell>
                <Table.Cell>{s.created_at ? new Date(s.created_at).toLocaleDateString() : '-'}</Table.Cell>
                <Table.Cell>
                  <Button size="mini" color="red" icon="trash" onClick={() => handleDelete(s.name)} />
                </Table.Cell>
              </Table.Row>
            ))}
          </Table.Body>
        </Table>
      </Segment>

      <Modal open={showCreate} onClose={() => setShowCreate(false)} size="small">
        <Modal.Header>Create Site</Modal.Header>
        <Modal.Content>
          <Form>
            <Form.Input label="Site Name" value={newSite.name} onChange={(e) => setNewSite({ ...newSite, name: e.target.value })} />
            <Form.Input label="Location" value={newSite.location} onChange={(e) => setNewSite({ ...newSite, location: e.target.value })} />
          </Form>
        </Modal.Content>
        <Modal.Actions>
          <Button onClick={() => setShowCreate(false)}>Cancel</Button>
          <Button primary onClick={handleCreate} disabled={!newSite.name}>Create</Button>
        </Modal.Actions>
      </Modal>
    </div>
  );
}
