import React, { useEffect, useState } from 'react';
import { Table, Header, Icon, Button, Segment, Label, Modal, Form } from 'semantic-ui-react';
import { endpoints } from '../api/endpoints';

export default function SecretsPage() {
  const [secrets, setSecrets] = useState<any[]>([]);
  const [showCreate, setShowCreate] = useState(false);
  const [newSecret, setNewSecret] = useState({ key: '', value: '', hidden: false });

  const load = () => endpoints.secrets.list().then((res) => setSecrets(res.data.items));

  useEffect(() => { load(); }, []);

  const handleCreate = async () => {
    await endpoints.secrets.create(newSecret.key, newSecret);
    setShowCreate(false);
    setNewSecret({ key: '', value: '', hidden: false });
    load();
  };

  const handleDelete = async (key: string) => {
    if (window.confirm(`Delete secret "${key}"?`)) {
      await endpoints.secrets.delete(key);
      load();
    }
  };

  return (
    <div>
      <Header as="h2"><Icon name="lock" /><Header.Content>Secrets<Header.Subheader>Secured variable storage</Header.Subheader></Header.Content></Header>
      <Segment>
        <div style={{ marginBottom: '1em' }}>
          <Button primary icon labelPosition="left" onClick={() => setShowCreate(true)}>
            <Icon name="plus" /> Create Secret
          </Button>
        </div>
        <Table celled striped>
          <Table.Header>
            <Table.Row>
              <Table.HeaderCell>Key</Table.HeaderCell>
              <Table.HeaderCell>Hidden</Table.HeaderCell>
              <Table.HeaderCell>Visibility</Table.HeaderCell>
              <Table.HeaderCell>Created By</Table.HeaderCell>
              <Table.HeaderCell>Updated</Table.HeaderCell>
              <Table.HeaderCell>Actions</Table.HeaderCell>
            </Table.Row>
          </Table.Header>
          <Table.Body>
            {secrets.map((s: any) => (
              <Table.Row key={s.key}>
                <Table.Cell><strong>{s.key}</strong></Table.Cell>
                <Table.Cell><Icon name={s.hidden ? 'eye slash' : 'eye'} color={s.hidden ? 'grey' : 'green'} /></Table.Cell>
                <Table.Cell><Label size="tiny">{s.visibility}</Label></Table.Cell>
                <Table.Cell>{s.created_by}</Table.Cell>
                <Table.Cell>{s.updated_at ? new Date(s.updated_at).toLocaleDateString() : '-'}</Table.Cell>
                <Table.Cell>
                  <Button size="mini" color="red" icon="trash" onClick={() => handleDelete(s.key)} />
                </Table.Cell>
              </Table.Row>
            ))}
          </Table.Body>
        </Table>
      </Segment>

      <Modal open={showCreate} onClose={() => setShowCreate(false)} size="small">
        <Modal.Header>Create Secret</Modal.Header>
        <Modal.Content>
          <Form>
            <Form.Input label="Key" value={newSecret.key} onChange={(e) => setNewSecret({ ...newSecret, key: e.target.value })} />
            <Form.Input label="Value" type="password" value={newSecret.value} onChange={(e) => setNewSecret({ ...newSecret, value: e.target.value })} />
            <Form.Checkbox label="Hidden" checked={newSecret.hidden} onChange={(e, d) => setNewSecret({ ...newSecret, hidden: !!d.checked })} />
          </Form>
        </Modal.Content>
        <Modal.Actions>
          <Button onClick={() => setShowCreate(false)}>Cancel</Button>
          <Button primary onClick={handleCreate} disabled={!newSecret.key}>Create</Button>
        </Modal.Actions>
      </Modal>
    </div>
  );
}
