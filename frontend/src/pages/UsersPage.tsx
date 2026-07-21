import React, { useEffect, useState } from 'react';
import { Table, Header, Icon, Button, Segment, Modal, Form, Label } from 'semantic-ui-react';
import { endpoints } from '../api/endpoints';

export default function UsersPage() {
  const [users, setUsers] = useState<any[]>([]);
  const [showCreate, setShowCreate] = useState(false);
  const [newUser, setNewUser] = useState({ username: '', password: 'changeme', role: 'user' });

  const load = () => endpoints.users.list().then((res) => setUsers(res.data.items));

  useEffect(() => { load(); }, []);

  const handleCreate = async () => {
    await endpoints.users.create(newUser);
    setShowCreate(false);
    setNewUser({ username: '', password: 'changeme', role: 'user' });
    load();
  };

  const handleDelete = async (username: string) => {
    if (window.confirm(`Delete user "${username}"?`)) {
      await endpoints.users.delete(username);
      load();
    }
  };

  return (
    <div>
      <Header as="h2"><Icon name="users" /><Header.Content>Users<Header.Subheader>User management</Header.Subheader></Header.Content></Header>
      <Segment>
        <div style={{ marginBottom: '1em' }}>
          <Button primary icon labelPosition="left" onClick={() => setShowCreate(true)}>
            <Icon name="plus" /> Create User
          </Button>
        </div>
        <Table celled striped>
          <Table.Header>
            <Table.Row>
              <Table.HeaderCell>Username</Table.HeaderCell>
              <Table.HeaderCell>Role</Table.HeaderCell>
              <Table.HeaderCell>Tenant</Table.HeaderCell>
              <Table.HeaderCell>Groups</Table.HeaderCell>
              <Table.HeaderCell>Created</Table.HeaderCell>
              <Table.HeaderCell>Actions</Table.HeaderCell>
            </Table.Row>
          </Table.Header>
          <Table.Body>
            {users.map((u: any) => (
              <Table.Row key={u.username}>
                <Table.Cell><strong>{u.username}</strong></Table.Cell>
                <Table.Cell><Label size="tiny" color={u.role === 'sys-admin' ? 'red' : 'blue'}>{u.role}</Label></Table.Cell>
                <Table.Cell>{u.tenant_name}</Table.Cell>
                <Table.Cell>{(u.groups || []).join(', ') || '-'}</Table.Cell>
                <Table.Cell>{u.created_at ? new Date(u.created_at).toLocaleDateString() : '-'}</Table.Cell>
                <Table.Cell>
                  <Button size="mini" color="red" icon="trash" onClick={() => handleDelete(u.username)} />
                </Table.Cell>
              </Table.Row>
            ))}
          </Table.Body>
        </Table>
      </Segment>

      <Modal open={showCreate} onClose={() => setShowCreate(false)} size="small">
        <Modal.Header>Create User</Modal.Header>
        <Modal.Content>
          <Form>
            <Form.Input label="Username" value={newUser.username} onChange={(e) => setNewUser({ ...newUser, username: e.target.value })} />
            <Form.Input label="Password" type="password" value={newUser.password} onChange={(e) => setNewUser({ ...newUser, password: e.target.value })} />
            <Form.Select label="Role" options={[{ text: 'User', value: 'user' }, { text: 'Admin', value: 'sys-admin' }]}
              value={newUser.role} onChange={(e, d) => setNewUser({ ...newUser, role: d.value as string })} />
          </Form>
        </Modal.Content>
        <Modal.Actions>
          <Button onClick={() => setShowCreate(false)}>Cancel</Button>
          <Button primary onClick={handleCreate} disabled={!newUser.username}>Create</Button>
        </Modal.Actions>
      </Modal>
    </div>
  );
}
