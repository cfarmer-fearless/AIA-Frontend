import React, { useState } from 'react';
import PropTypes from 'prop-types';
import { useTable, useFilters, useSortBy } from 'react-table';

export default function Table({ columns, data }) {
  const [filterInput, setFilterInput] = useState('');
  const {
    getTableProps,
    getTableBodyProps,
    headerGroups,
    rows,
    prepareRow,
    setFilter,
  } = useTable(
    {
      columns,
      data,
    },
    useFilters,
    useSortBy
  );

  const handleFilterChange = (e) => {
    const value = e.target.value || undefined;
    setFilter('id', value);
    setFilterInput(value);
  };

  return (
    <>
      <input
        value={filterInput}
        onChange={handleFilterChange}
        placeholder={'Search ID'}
      />
      <table {...getTableProps()}>
        <thead>
          {headerGroups.map((headerGroup) => (
            <tr key={headerGroup.id} {...headerGroup.getHeaderGroupProps()}>
              {headerGroup.headers.map((column) => (
                <th
                  {...column.getHeaderProps(column.getSortByToggleProps())}
                  key={column.id}
                  className={
                    column.isSorted
                      ? column.isSortedDesc
                        ? 'sort-desc'
                        : 'sort-asc'
                      : ''
                  }
                >
                  {column.render('Header')}
                </th>
              ))}
            </tr>
          ))}
        </thead>
        <tbody {...getTableBodyProps()}>
          {rows.map((row) => {
            prepareRow(row);
            return (
              <tr key={row.id} {...row.getRowProps()}>
                {row.cells.map((cell, i) => {
                  return (
                    <td key={i} {...cell.getCellProps()}>
                      {cell.render('Cell')}
                    </td>
                  );
                })}
              </tr>
            );
          })}
        </tbody>
      </table>
    </>
  );
}

Table.propTypes = {
  columns: PropTypes.arrayOf(
    PropTypes.shape({ Header: PropTypes.string, accessor: PropTypes.string })
  ).isRequired,
  data: PropTypes.arrayOf(PropTypes.object).isRequired,
};
