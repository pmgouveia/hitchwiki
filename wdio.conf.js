exports.config = {
    specs: [
        './tests/features/**/*.feature',
    ],
    exclude: [
        // 'path/to/excluded/files'
    ],
    
    maxInstances: 5,
    
    capabilities: [{
        maxInstances: 5,
        browserName: 'chrome',
    }],
    
    sync: true,
    logLevel: 'error',
    
    coloredLogs: true,
    
    screenshotPath: './tests/',
    
    baseUrl: 'http://localhost:8080',
    
    waitforTimeout: 10000,
    
    connectionRetryTimeout: 90000,
    
    connectionRetryCount: 3,
    
    services: ['selenium-standalone'],
    
    framework: 'cucumber',
    
    reporters: ['spec'],
    
    cucumberOpts: {
        require: [
            './tests/cucumber-boilerplate/src/steps/given.js',
            './tests/cucumber-boilerplate/src/steps/when.js',
            './tests/cucumber-boilerplate/src/steps/then.js',
        ], // <string[]> (file/dir) require files before executing features
        backtrace: false, // <boolean> show full backtrace for errors
        compiler: [
            'js:babel-register',
        ], // <string[]> ("extension:module") require files with the given
    
        dryRun: false, // <boolean> invoke formatters without executing steps
        failFast: false, // <boolean> abort the run on first failure
        format: ['pretty'], // <string[]> (type[:path]) specify the output
                            // format, optionally supply PATH to redirect
                            // formatter output (repeatable)
        colors: true, // <boolean> disable colors in formatter output
        snippets: true, // <boolean> hide step definition snippets for pending
        source: true, // <boolean> hide source uris
        profile: [], // <string[]> (name) specify the profile to use
        strict: true, // <boolean> fail if there are any undefined or pending
                       // steps
        tags: require('./tests/cucumber-boilerplate/src/tagProcessor')(process.argv),
        timeout: 20000,     // <number> timeout for step definitions
        ignoreUndefinedDefinitions: false,
    },
    before: function before() {
        const chai = require('chai');

        global.expect = chai.expect;
        global.assert = chai.assert;
        global.should = chai.should();
    },
};
