

RECI.PY
=======

Reci.py is a build system. It is focused on describing the file tree as it
should be after the build. Build files are XML:

    <folder name="dist" xmlns="http://recipy.hoverview.org/default">
      <zipfile filename="myapp.war">
        <folder name="WEB-INF">
          <copies of="src/main/webapp/web.xml"/>
        </folder>
      </zipfile>
    </folder>

This approach is meant to give a clear view of build results with a lot of
flexibility at low complexity. The default xml namespace handles things like
creating a folder and copying static files there. Other namespaces can be
used by installing (with git clone or other mechanism) a vocabulary module
into the vocab lib folder in the reci.py installation. Vocabularies are Python
modules that follow a simple set of conventions. 
