import React, { useEffect, useState } from 'react';
import { Table, Header, Icon, Button, Segment, Label, Modal, Form } from 'semantic-ui-react';
import { endpoints } from '../api/endpoints';

export default function PluginsPage() {
  const [plugins, setPlugins] = useState<any[]>([]);
  const [showUpload, setShowUpload] = useState(false);
  const [newPlugin, setNewPlugin] = useState({ id: '', package_name: '', package_version: '1.0.0' });

  const load = () => endpoints.plugins.list().then((res) => setPlugins(res.data.items));

  useEffect(() => { load(); }, []);

  const handleUpload = async () => {
    await endpoints.plugins.upload(newPlugin.id, newPlugin);
    setShowUpload(false);
    setNewPlugin({ id: '', package_name: '', package_version: '1.0.0' });
    load();
  };

  const handleDelete = async (id: string) => {
    if (window.confirm(`Delete plugin "${id}"?`)) {
      await endpoints.plugins.delete(id);
      load();
    }
  };

  return (
    <div>
      <Header as="h2"><Icon name="puzzle piece" /><Header.Content>Plugins<Header.Subheader>Manage Conductor plugins</Header.Subheader></Header.Content></Header>
      <Segment>
        <div style={{ marginBottom: '1em' }}>
          <Button primary icon labelPosition="left" onClick={() => setShowUpload(true)}>
            <Icon name="upload" /> Upload Plugin
          </Button>
        </div>
        <Table celled striped>
          <Table.Header>
            <Table.Row>
              <Table.HeaderCell>Plugin ID</Table.HeaderCell>
              <Table.HeaderCell>Package</Table.HeaderCell>
              <Table.HeaderCell>Version</Table.HeaderCell>
              <Table.HeaderCell>Platform</Table.HeaderCell>
              <Table.HeaderCell>Visibility</Table.HeaderCell>
              <Table.HeaderCell>Uploaded</Table.HeaderCell>
              <Table.HeaderCell>Actions</Table.HeaderCell>
            </Table.Row>
          </Table.Header>
          <Table.Body>
            {plugins.map((p: any) => (
              <Table.Row key={p.id}>
                <Table.Cell><strong>{p.id}</strong></Table.Cell>
                <Table.Cell>{p.package_name}</Table.Cell>
                <Table.Cell>{p.package_version}</Table.Cell>
                <Table.Cell>{p.supported_platform}</Table.Cell>
                <Table.Cell><Label size="tiny">{p.visibility}</Label></Table.Cell>
                <Table.Cell>{p.uploaded_at ? new Date(p.uploaded_at).toLocaleDateString() : '-'}</Table.Cell>
                <Table.Cell>
                  <Button size="mini" color="red" icon="trash" onClick={() => handleDelete(p.id)} />
                </Table.Cell>
              </Table.Row>
            ))}
          </Table.Body>
        </Table>
      </Segment>

      <Modal open={showUpload} onClose={() => setShowUpload(false)} size="small">
        <Modal.Header>Upload Plugin</Modal.Header>
        <Modal.Content>
          <Form>
            <Form.Input label="Plugin ID" value={newPlugin.id} onChange={(e) => setNewPlugin({ ...newPlugin, id: e.target.value })} />
            <Form.Input label="Package Name" value={newPlugin.package_name} onChange={(e) => setNewPlugin({ ...newPlugin, package_name: e.target.value })} />
            <Form.Input label="Version" value={newPlugin.package_version} onChange={(e) => setNewPlugin({ ...newPlugin, package_version: e.target.value })} />
          </Form>
        </Modal.Content>
        <Modal.Actions>
          <Button onClick={() => setShowUpload(false)}>Cancel</Button>
          <Button primary onClick={handleUpload} disabled={!newPlugin.id}>Upload</Button>
        </Modal.Actions>
      </Modal>
    </div>
  );
}
