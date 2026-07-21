import React, { useEffect, useState } from 'react';
import { Table, Header, Icon, Button, Segment, Modal, Form } from 'semantic-ui-react';
import { endpoints } from '../api/endpoints';

export default function FiltersPage() {
  const [filters, setFilters] = useState<any[]>([]);
  const [showCreate, setShowCreate] = useState(false);
  const [newFilter, setNewFilter] = useState({ id: '', blueprint_id: '', deployment_id: '' });

  const load = () => endpoints.filters.list().then((res) => setFilters(res.data.items));

  useEffect(() => { load(); }, []);

  const handleCreate = async () => {
    await endpoints.filters.create(newFilter);
    setShowCreate(false);
    setNewFilter({ id: '', blueprint_id: '', deployment_id: '' });
    load();
  };

  const handleDelete = async (id: string) => {
    if (window.confirm(`Delete filter "${id}"?`)) {
      await endpoints.filters.delete(id);
      load();
    }
  };

  return (
    <div>
      <Header as="h2"><Icon name="filter" /><Header.Content>Filters<Header.Subheader>Resource and event filters</Header.Subheader></Header.Content></Header>
      <Segment>
        <div style={{ marginBottom: '1em' }}>
          <Button primary icon labelPosition="left" onClick={() => setShowCreate(true)}>
            <Icon name="plus" /> Create Filter
          </Button>
        </div>
        <Table celled striped>
          <Table.Header>
            <Table.Row>
              <Table.HeaderCell>Filter ID</Table.HeaderCell>
              <Table.HeaderCell>Blueprint</Table.HeaderCell>
              <Table.HeaderCell>Deployment</Table.HeaderCell>
              <Table.HeaderCell>Execution</Table.HeaderCell>
              <Table.HeaderCell>Rules</Table.HeaderCell>
              <Table.HeaderCell>Created</Table.HeaderCell>
              <Table.HeaderCell>Actions</Table.HeaderCell>
            </Table.Row>
          </Table.Header>
          <Table.Body>
            {filters.map((f: any) => (
              <Table.Row key={f.id}>
                <Table.Cell><strong>{f.id}</strong></Table.Cell>
                <Table.Cell>{f.blueprint_id || '-'}</Table.Cell>
                <Table.Cell>{f.deployment_id || '-'}</Table.Cell>
                <Table.Cell>{f.execution_id || '-'}</Table.Cell>
                <Table.Cell style={{ maxWidth: 200, overflow: 'hidden', textOverflow: 'ellipsis' }}>
                  {JSON.stringify(f.rules || {})}
                </Table.Cell>
                <Table.Cell>{f.created_at ? new Date(f.created_at).toLocaleDateString() : '-'}</Table.Cell>
                <Table.Cell>
                  <Button size="mini" color="red" icon="trash" onClick={() => handleDelete(f.id)} />
                </Table.Cell>
              </Table.Row>
            ))}
          </Table.Body>
        </Table>
      </Segment>

      <Modal open={showCreate} onClose={() => setShowCreate(false)} size="small">
        <Modal.Header>Create Filter</Modal.Header>
        <Modal.Content>
          <Form>
            <Form.Input label="Filter ID" value={newFilter.id} onChange={(e) => setNewFilter({ ...newFilter, id: e.target.value })} />
            <Form.Input label="Blueprint ID" value={newFilter.blueprint_id} onChange={(e) => setNewFilter({ ...newFilter, blueprint_id: e.target.value })} />
            <Form.Input label="Deployment ID" value={newFilter.deployment_id} onChange={(e) => setNewFilter({ ...newFilter, deployment_id: e.target.value })} />
          </Form>
        </Modal.Content>
        <Modal.Actions>
          <Button onClick={() => setShowCreate(false)}>Cancel</Button>
          <Button primary onClick={handleCreate} disabled={!newFilter.id}>Create</Button>
        </Modal.Actions>
      </Modal>
    </div>
  );
}
