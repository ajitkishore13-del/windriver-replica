import React, { useEffect, useState } from 'react';
import { Table, Header, Icon, Button, Segment, Modal, Form } from 'semantic-ui-react';
import { endpoints } from '../api/endpoints';

export default function TenantsPage() {
  const [tenants, setTenants] = useState<any[]>([]);
  const [showCreate, setShowCreate] = useState(false);
  const [newTenant, setNewTenant] = useState({ name: '' });

  const load = () => endpoints.tenants.list().then((res) => setTenants(res.data.items));

  useEffect(() => { load(); }, []);

  const handleCreate = async () => {
    await endpoints.tenants.create(newTenant);
    setShowCreate(false);
    setNewTenant({ name: '' });
    load();
  };

  const handleDelete = async (name: string) => {
    if (window.confirm(`Delete tenant "${name}"?`)) {
      await endpoints.tenants.delete(name);
      load();
    }
  };

  return (
    <div>
      <Header as="h2"><Icon name="building" /><Header.Content>Tenants<Header.Subheader>Multi-tenancy management</Header.Subheader></Header.Content></Header>
      <Segment>
        <div style={{ marginBottom: '1em' }}>
          <Button primary icon labelPosition="left" onClick={() => setShowCreate(true)}>
            <Icon name="plus" /> Create Tenant
          </Button>
        </div>
        <Table celled striped>
          <Table.Header>
            <Table.Row>
              <Table.HeaderCell>Tenant Name</Table.HeaderCell>
              <Table.HeaderCell>Created</Table.HeaderCell>
              <Table.HeaderCell>Actions</Table.HeaderCell>
            </Table.Row>
          </Table.Header>
          <Table.Body>
            {tenants.map((t: any) => (
              <Table.Row key={t.name}>
                <Table.Cell><strong>{t.name}</strong></Table.Cell>
                <Table.Cell>{t.created_at ? new Date(t.created_at).toLocaleDateString() : '-'}</Table.Cell>
                <Table.Cell>
                  <Button size="mini" color="red" icon="trash" onClick={() => handleDelete(t.name)} />
                </Table.Cell>
              </Table.Row>
            ))}
          </Table.Body>
        </Table>
      </Segment>

      <Modal open={showCreate} onClose={() => setShowCreate(false)} size="small">
        <Modal.Header>Create Tenant</Modal.Header>
        <Modal.Content>
          <Form>
            <Form.Input label="Tenant Name" value={newTenant.name} onChange={(e) => setNewTenant({ ...newTenant, name: e.target.value })} />
          </Form>
        </Modal.Content>
        <Modal.Actions>
          <Button onClick={() => setShowCreate(false)}>Cancel</Button>
          <Button primary onClick={handleCreate} disabled={!newTenant.name}>Create</Button>
        </Modal.Actions>
      </Modal>
    </div>
  );
}
