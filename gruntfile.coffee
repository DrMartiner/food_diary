module.exports = (grunt) ->
    grunt.initConfig
        pkg: grunt.file.readJSON 'package.json'
        watch:
            coffee:
                files: ['static/coffee/**/*.coffee']
                tasks: ['coffee:dist']
            less:
                files: ['static/css/**/*.less']
                tasks: ['less:dist']
        coffee:
            dist:
                files: [{
                    expand: true,
                    cwd: 'static/coffee',
                    src: '**/*.coffee',
                    dest: 'static/js',
                    ext: '.js'
                }]
        less:
            dist:
                options:
                    paths: ["static/css/less"]
                files:
                    "static/css/screen.css": "static/css/less/screen.less"

    grunt.loadNpmTasks 'grunt-contrib-coffee'
    grunt.loadNpmTasks 'grunt-contrib-watch'
    grunt.loadNpmTasks 'grunt-contrib-less'

    grunt.registerTask 'run', [
        'coffee:dist',
        'less:dist',
        'watch'
    ]