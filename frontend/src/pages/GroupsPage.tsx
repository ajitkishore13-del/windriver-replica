import React, { useEffect, useState } from 'react';
import { Table, Header, Icon, Button, Segment, Modal, Form, Label } from 'semantic-ui-react';
import { endpoints } from '../api/endpoints';

export default function GroupsPage() {
  const [groups, setGroups] = useState<any[]>([]);
  const [showCreate, setShowCreate] = useState(false);
  const [newGroup, setNewGroup] = useState({ name: '', role: 'user' });

  const load = () => endpoints.groups.list().then((res) => setGroups(res.data.items));

  useEffect(() => { load(); }, []);

  const handleCreate = async () => {
    await endpoints.groups.create(newGroup);
    setShowCreate(false);
    setNewGroup({ name: '', role: 'user' });
    load();
  };

  const handleDelete = async (name: string) => {
    if (window.confirm(`Delete group "${name}"?`)) {
      await endpoints.groups.delete(name);
      load();
    }
  };

  return (
    <div>
      <Header as="h2"><Icon name="group" /><Header.Content>Groups<Header.Subheader>User group management</Header.Subheader></Header.Content></Header>
      <Segment>
        <div style={{ marginBottom: '1em' }}>
          <Button primary icon labelPosition="left" onClick={() => setShowCreate(true)}>
            <Icon name="plus" /> Create Group
          </Button>
        </div>
        <Table celled striped>
          <Table.Header>
            <Table.Row>
              <Table.HeaderCell>Name</Table.HeaderCell>
              <Table.HeaderCell>Role</Table.HeaderCell>
              <Table.HeaderCell>Tenant</Table.HeaderCell>
              <Table.HeaderCell>LDAP</Table.HeaderCell>
              <Table.HeaderCell>Users</Table.HeaderCell>
              <Table.HeaderCell>Created</Table.HeaderCell>
              <Table.HeaderCell>Actions</Table.HeaderCell>
            </Table.Row>
          </Table.Header>
          <Table.Body>
            {groups.map((g: any) => (
              <Table.Row key={g.name}>
                <Table.Cell><strong>{g.name}</strong></Table.Cell>
                <Table.Cell><Label size="tiny">{g.role}</Label></Table.Cell>
                <Table.Cell>{g.tenant_name}</Table.Cell>
                <Table.Cell>{g.ldap_group ? <Icon name="check" color="green" /> : <Icon name="times" color="grey" />}</Table.Cell>
                <Table.Cell>{(g.users || []).join(', ') || '-'}</Table.Cell>
                <Table.Cell>{g.created_at ? new Date(g.created_at).toLocaleDateString() : '-'}</Table.Cell>
                <Table.Cell>
                  <Button size="mini" color="red" icon="trash" onClick={() => handleDelete(g.name)} />
                </Table.Cell>
              </Table.Row>
            ))}
          </Table.Body>
        </Table>
      </Segment>

      <Modal open={showCreate} onClose={() => setShowCreate(false)} size="small">
        <Modal.Header>Create Group</Modal.Header>
        <Modal.Content>
          <Form>
            <Form.Input label="Group Name" value={newGroup.name} onChange={(e) => setNewGroup({ ...newGroup, name: e.target.value })} />
            <Form.Select label="Role" options={[{ text: 'User', value: 'user' }, { text: 'Admin', value: 'sys-admin' }]}
              value={newGroup.role} onChange={(e, d) => setNewGroup({ ...newGroup, role: d.value as string })} />
          </Form>
        </Modal.Content>
        <Modal.Actions>
          <Button onClick={() => setShowCreate(false)}>Cancel</Button>
          <Button primary onClick={handleCreate} disabled={!newGroup.name}>Create</Button>
        </Modal.Actions>
      </Modal>
    </div>
  );
}
