import React, { useEffect, useState } from 'react';
import { Table, Header, Icon, Button, Segment, Label } from 'semantic-ui-react';
import { endpoints } from '../api/endpoints';

export default function SnapshotsPage() {
  const [snapshots, setSnapshots] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);

  const load = () => endpoints.snapshots.list().then((res) => setSnapshots(res.data.items));

  useEffect(() => { load(); }, []);

  const handleCreate = async () => {
    setLoading(true);
    await endpoints.snapshots.create();
    await load();
    setLoading(false);
  };

  const handleDelete = async (id: string) => {
    if (window.confirm(`Delete snapshot "${id}"?`)) {
      await endpoints.snapshots.delete(id);
      load();
    }
  };

  return (
    <div>
      <Header as="h2"><Icon name="camera" /><Header.Content>Snapshots<Header.Subheader>System snapshots management</Header.Subheader></Header.Content></Header>
      <Segment>
        <div style={{ marginBottom: '1em' }}>
          <Button primary icon labelPosition="left" loading={loading} onClick={handleCreate}>
            <Icon name="plus" /> Create Snapshot
          </Button>
        </div>
        <Table celled striped>
          <Table.Header>
            <Table.Row>
              <Table.HeaderCell>Snapshot ID</Table.HeaderCell>
              <Table.HeaderCell>Status</Table.HeaderCell>
              <Table.HeaderCell>Created By</Table.HeaderCell>
              <Table.HeaderCell>Created</Table.HeaderCell>
              <Table.HeaderCell>Actions</Table.HeaderCell>
            </Table.Row>
          </Table.Header>
          <Table.Body>
            {snapshots.map((s: any) => (
              <Table.Row key={s.id}>
                <Table.Cell><strong>{s.id}</strong></Table.Cell>
                <Table.Cell><Label size="tiny" color={s.status === 'created' ? 'green' : 'grey'}>{s.status}</Label></Table.Cell>
                <Table.Cell>{s.created_by}</Table.Cell>
                <Table.Cell>{s.created_at ? new Date(s.created_at).toLocaleDateString() : '-'}</Table.Cell>
                <Table.Cell>
                  <Button size="mini" color="red" icon="trash" onClick={() => handleDelete(s.id)} />
                </Table.Cell>
              </Table.Row>
            ))}
          </Table.Body>
        </Table>
      </Segment>
    </div>
  );
}
