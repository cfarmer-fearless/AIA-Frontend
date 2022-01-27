import React from 'react';
import './button.css';

interface ButtonProps {
  label: string;
  backgroundColor?: string;
  primary?: boolean;
  size?: string;
  [prop: string]: any
}

/**
 * Primary UI component for user interaction
 */
export const Button: React.FC<ButtonProps> = ({ label, primary = false, backgroundColor = undefined, size = 'medium', ...props }) => {
  const mode = primary ? 'storybook-button--primary' : 'storybook-button--secondary';
  return (
    <button
      type="button"
      className={['storybook-button', `storybook-button--${size}`, `storybook-button--${backgroundColor}`, mode].join(' ')}
      {...props}
    >
      {label}
    </button>
  );
};
