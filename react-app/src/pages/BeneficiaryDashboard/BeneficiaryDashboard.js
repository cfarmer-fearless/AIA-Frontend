import React, { useMemo, useState, useEffect } from 'react';
import Table from '../../components/Table/Table';
import useToken from '../../hooks/useToken';
import CircularProgress from '@mui/material/CircularProgress';
import Dialog from '@mui/material/Dialog';

const Records = ({ values }) => {
  return (
    <>
      {values.map((record) => <BadgeComponent record={record}/>)}
    </>
  );
};

function BadgeComponent(props){

  const record = props.record;

  const [visible, setVisible] = useState(false);

  function textAltWrapper(content){
    if(content === undefined || content === null || content === ''){
      return 'N/A';
    }
    return content;
  }

  function textAltWrapperDateRange(startDate, endDate){
    if(startDate !== undefined && startDate !== ''){
      if(endDate !== undefined && endDate !== ''){
        return (startDate + ' to ' + endDate);
      }
      else {
        return (startDate + ' to Present');
      }
    }
    else {
      return 'N/A';
    }
  }




  return (
    <span key={record.id} className="badge">
      {'Coverage Effective Date: ' + record.coverageEffectiveDate}
      <br />
      {'Dialysis Effective Date: ' + record.dialysisEffectiveDate}
      <br />
      {'Dialysis Termination Date: ' + record.dialysisTerminationDate}
      <br />
      <div className={'beneficiary-more-info-link'} onClick={() => setVisible(true)}>More Info</div>
      <Dialog onClose={() => setVisible(false)} open={visible}>
        <div className={'beneficiary-more-info-dialog-container'}>
          <div className={'beneficiary-more-info-dialog-title'}>Dialysis Event</div>
          <div>Beneficiary ID: {record.beneficiaryId}</div>
          <div>Coverage From: {textAltWrapperDateRange(record.coverageEffectiveDate, record.coverageTerminationDate)}</div>
          <div>Dialysis From: {textAltWrapperDateRange(record.dialysisEffectiveDate, record.dialysisTerminationDate)}</div>
          <div>Coverage Termination Reason: {textAltWrapper(record.terminationReason)}</div>
          <div>Coverage Period: {textAltWrapper(record.coveragePeriod)}</div>
          <div>Coverage Source: {textAltWrapper(record.coverageSource)}</div>
          <div>Transplant From: {textAltWrapperDateRange(record.transplantEffectiveDate, record.transplateTerminationDate)}</div>  
        </div>
      </Dialog>
    </span>
  );
}

function BeneficiaryDashboard() {
  const columns = useMemo(
    () => [
      {
        Header: 'Beneficiary',
        columns: [
          {
            Header: 'Id',
            accessor: 'id'
          },
          {
            Header: 'First Name',
            accessor: 'name.firstName'
          },
          {
            Header: 'Last Name',
            accessor: 'name.lastName'
          },
          {
            Header: 'Date of Birth',
            accessor: 'dateOfBirth'
          }
        ]
      },
      {
        Header: 'ESRD Data',
        columns: [
          {
            Header: 'Dialysis Records',
            accessor: 'dialysisRecords',
            Cell: ({ cell: { value } }) => <Records values={value} />
          }
        ]
      }
    ],
    []
  );

  const [data, setData] = useState([]);
  const token = useToken();

  useEffect(() => {
    const { REACT_APP_BEN_API_ENDPOINT } = process.env;
    fetch(REACT_APP_BEN_API_ENDPOINT, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': token.token
      }
    })
      .then(response => response.json())
      .then(data => {
        setData(data);
        console.log(data);
      });
  }, [token.token]);

  console.log('data',data);

  return (
    <div className={'beneficiary-dashboard'}>
      <h2>Welcome to the Beneficiary Dashboard</h2>
      
      {
        data.length === 0
          ? 
          <div className={'beneficiary-dashboard-loading-container'}>
            <CircularProgress />
            <div>Beneficiary Data is Loading</div>
            {console.log('in primary part')}
          </div>
          :
        
          <div className="BeneficiaryDashboard">
            <Table columns={columns} data={data} />
            {console.log('in secondary part')}
          </div>
      } 
    </div>
  );
}

export default BeneficiaryDashboard;