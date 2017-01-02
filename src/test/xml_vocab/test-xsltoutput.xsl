<t:transform
  version="1.0"
  xmlns:t="http://www.w3.org/1999/XSL/Transform">
  <t:output method="text" omit-xml-declaration="yes" indent="no"/>
  <t:template match="/root">
    <t:value-of select="someelement"/>
  </t:template>
</t:transform>