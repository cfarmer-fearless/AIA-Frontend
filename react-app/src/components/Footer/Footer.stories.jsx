import React from 'react';
import { Footer } from './Footer';

export default {
  title: 'Components/Footer',
  component: Footer,
};

const Template = (args) => <Footer {...args} />;

export const Example = Template.bind({});
Example.args = {
  text: "© 2021 Example Footer"
};

export const Default = Template.bind({});
Default.args = {};
