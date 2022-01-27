import { render, screen } from '@testing-library/react';
import App from './App';
import BeneficiaryDashboard from './components/BeneficiaryDashboard';
import NotFound from './components/NotFound';
import { MemoryRouter } from 'react-router-dom';

beforeEach(() => {
  sessionStorage.clear();
});

test('renders Login page', () => {
  render(<App />);
  const button = screen.getByText(/Submit/i);
  expect(button).toBeInTheDocument();
});

test('renders the Beneficiary Dashboard', () => {
  render(<BeneficiaryDashboard />);
  const header = screen.getByText('Welcome to the Beneficiary Dashboard');
  expect(header).toBeInTheDocument();
});

test('renders a generic 404 page', () => {
  render(
    <MemoryRouter>
      <NotFound/>
    </MemoryRouter>
  );
  const header = screen.getByText('404 - Page Not Found!');
  expect(header).toBeInTheDocument();
});

test('renders a 404 page when hitting bad routes', () => {
  sessionStorage.setItem('token', JSON.stringify('sometoken'));
  render(
    <MemoryRouter initialEntries={['/somerandomroute']} initialIndex={0}>
      <App />
    </MemoryRouter>
  );
  const header = screen.getByText('404 - Page Not Found!');
  expect(header).toBeInTheDocument();
});

test('renders Beneficiaries dashboard when authenticated', () => {
  sessionStorage.setItem('token', JSON.stringify('sometoken'));
  render(
    <MemoryRouter initialEntries={['/beneficiaries']}>
      <App />
    </MemoryRouter>
  );
  const header = screen.getByText('Welcome to the Beneficiary Dashboard');
  expect(header).toBeInTheDocument();
});
