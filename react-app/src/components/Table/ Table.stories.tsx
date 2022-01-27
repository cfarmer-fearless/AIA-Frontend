import React from 'react';
import Table from './Table';

export default {
  title: 'Components/Table',
  component: Table,
};

const Template = (args) => <Table {...args} />;

export const Example = Template.bind({});
Example.args = {
  columns: [
    {
      Header: 'ID',
      accessor: 'id',
    },
    {
      Header: 'Column A',
      accessor: 'colA',
    },
    {
      Header: 'Column B',
      accessor: 'colB',
    },
  ],
  data: [
    {
      id: 123,
      colA: 'a1',
      colB: 'b1'
    }, {
      id: 456,
      colA: 'a2',
      colB: 'b2'
    }
  ]
};
