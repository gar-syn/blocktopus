import builtins from 'rollup-plugin-node-builtins';
import multiEntry from '@rollup/plugin-multi-entry';

export default [{
  // core input options
  input: {
    include: [
      'blocktopus/blockly/core/blockly.js',
      'blocktopus/blockly/blocks/*.js',
    ],
    exclude: [
      'blocktopus/blockly/blocks/mixins.js',
      'blocktopus/blockly/blocks/lists.js'
    ]
  },
  output: {
    file: 'blocktopus/resources/blockly/pack/blockly.js',
    format: 'iife',
    name: 'Blockly',
    globals: {
      tinycolor: 'tinycolor'
    }
  },
  plugins: [
    builtins(), 
    multiEntry()
  ]
}, {
  input: {
    include: [
      'blocktopus/blockly/generators/python-octo.js',
      'blocktopus/blockly/generators/python-octo/*.js',
    ],
    exclude: [
      'blocktopus/blockly/generators/python-octo/lists.js',
    ]
  },
  plugins: [
    multiEntry()
  ],
  output: {
    file: 'blocktopus/resources/blockly/pack/octopus-generator.js',
    format: 'iife',
    name: 'PythonOctoGenerator',
    globals: {
      Blockly: 'Blockly'
    }
  }
}, {
  input: 'blocktopus/blockly/msg/messages.js',
  output: {
    file: 'blocktopus/resources/blockly/pack/blockly-messages.js',
    format: 'iife',
    name: 'Blockly.Msg',
    globals: {
      Blockly: 'Blockly'
    }
  }
}];
