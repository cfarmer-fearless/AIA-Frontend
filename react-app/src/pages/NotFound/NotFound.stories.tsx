import React from 'react';
import StoryRouter from 'storybook-react-router';
import NotFound from './NotFound';

export default {
  title: 'Pages/NotFound',
  component: NotFound,
  decorators: [StoryRouter()],
};

export const Default = () => <NotFound />;
