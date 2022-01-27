import React from 'react';
import { Header } from './Header';

export default {
  title: 'Components/Header',
  component: Header,
};

const Template = (args) => <Header {...args} />;

export const LoggedIn = Template.bind({});
LoggedIn.args = {
  user: {},
  title: "Example Header"
};

export const LoggedOut = Template.bind({});
LoggedOut.args = {
  title: "Example Header"
};
