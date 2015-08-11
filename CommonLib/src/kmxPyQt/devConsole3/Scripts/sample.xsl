<xsl:stylesheet version="1.0"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:xs="http://www.w3.org/2001/XMLSchema"
  xmlns:json="http://www.ibm.com/xmlns/prod/2009/jsonx"
  xmlns:exsl="http://exslt.org/common"
  xmlns:so="http://stackoverflow.com/questions/13007280"
  exclude-result-prefixes="xsl xs json so exsl">
<xsl:output indent="yes" encoding="UTF-8" omit-xml-declaration="yes" />
<xsl:strip-space elements="*" /> 

<xsl:variable name="quot" select="'&quot;'" />

<xsl:template match="/*">
  <xsl:variable name="t1">
    <xsl:call-template name="object">
     <xsl:with-param name="json-in" select="." />
    </xsl:call-template>
  </xsl:variable>
  <xsl:apply-templates select="exsl:node-set($t1)/so:output/*" mode="copy-sans-namespace" />  
</xsl:template>

<xsl:template match="*" mode="copy-sans-namespace">
  <xsl:element name="{name()}" namespace="{namespace-uri()}">
    <xsl:copy-of select="@*"/>
    <xsl:apply-templates mode="copy-sans-namespace" />
  </xsl:element>
</xsl:template>

<xsl:template name="field">
  <!-- Input like: "Open": "25.15" bla -->
  <!-- output like: <so:output><Open>25.15</Open></so:output> <so:extra>bla</so:extra> -->
  <xsl:param name="json-in" />
  <xsl:variable name="field-name" select="substring-before(substring-after($json-in,$quot),$quot)" />
  <xsl:variable name="remainder" select="substring-after($json-in,':')" />
  <xsl:call-template name="value">
    <xsl:with-param name="json-in" select="$remainder" />
    <xsl:with-param name="parent-ele" select="$field-name" />
  </xsl:call-template>
</xsl:template>

<xsl:template name="fields">
  <!-- Input like: "Open": "25.15" , "High": "25.15" } bla -->
  <!-- output like: <so:output><Open>25.15</Open><High>25.15</High></so:output> <so:extra>} bla</so:extra> -->
  <xsl:param name="json-in" />
  <xsl:variable name="n" select="normalize-space($json-in)" />
  <xsl:choose>
    <xsl:when test="substring($n,1,1) = $quot">
    <xsl:variable name="t1">
        <xsl:call-template name="field">
          <xsl:with-param name="json-in" select="$n" />
      </xsl:call-template>
    </xsl:variable>
    <xsl:variable name="t2" select="normalize-space( exsl:node-set($t1)/so:extra) " />
    <xsl:variable name="t3">
      <xsl:choose>
      <xsl:when test="substring($t2,1,1)=','">
            <xsl:call-template name="fields">
              <xsl:with-param name="json-in" select="substring-after($t2,',')" />
          </xsl:call-template>
      </xsl:when>
      <xsl:when test="$t2">
        <so:extra><xsl:value-of select="$t2" /></so:extra>
      </xsl:when>
      </xsl:choose>
    </xsl:variable>
    <so:output>
      <xsl:copy-of select="exsl:node-set($t1)/so:output/* | exsl:node-set($t3)/so:output/*" />
    </so:output>
    <xsl:copy-of select="exsl:node-set($t3)/so:extra" />
  </xsl:when>
    <xsl:when test="$n">
      <so:extra><xsl:value-of select="$n" /></so:extra>
    </xsl:when>
  </xsl:choose>
</xsl:template>

<xsl:template name="object">
  <!-- Input like: { X } bla -->
  <!-- output like: <so:output>fields(X)</so:output> <so:extra>bla</so:extra> -->
  <xsl:param name="json-in" />
  <xsl:param name="parent-ele" select="''" />
  <xsl:variable name="t1" select="normalize-space(substring-after($json-in,'{'))" />
  <xsl:variable name="t2">
    <xsl:call-template name="fields">
      <xsl:with-param name="json-in" select="$t1" />
    </xsl:call-template>
  </xsl:variable>  
  <xsl:variable name="t3" select="normalize-space(substring-after( exsl:node-set($t2)/so:extra, '}'))" />
  <so:output>
    <xsl:choose>
    <xsl:when test="$parent-ele">
      <xsl:element name="{$parent-ele}">
        <xsl:copy-of select="exsl:node-set($t2)/so:output/node()" />
      </xsl:element>
    </xsl:when>
      <xsl:otherwise>    
        <xsl:copy-of select="exsl:node-set($t2)/so:output/node()" />
      </xsl:otherwise>    
    </xsl:choose>
  </so:output>
  <xsl:if test="$t3">
    <so:extra><xsl:value-of select="$t3" /></so:extra>
  </xsl:if>  
</xsl:template>

<xsl:template name="objects">
  <xsl:param name="json-in" />
  <xsl:param name="parent-ele" />
  <xsl:variable name="n" select="normalize-space($json-in)" />
  <xsl:choose>
    <xsl:when test="substring($n,1,1) = '{'">
    <xsl:variable name="t1">
        <xsl:call-template name="object">
          <xsl:with-param name="json-in" select="$n" />
          <xsl:with-param name="parent-ele" select="$parent-ele" />
      </xsl:call-template>
    </xsl:variable>
    <xsl:variable name="t2" select="normalize-space( exsl:node-set($t1)/so:extra) " />
    <xsl:variable name="t3">
      <xsl:choose>
      <xsl:when test="substring($t2,1,1)='{'">
            <xsl:call-template name="objects">
              <xsl:with-param name="json-in" select="$t2" />
              <xsl:with-param name="parent-ele" select="$parent-ele" />
          </xsl:call-template>
      </xsl:when>
      <xsl:when test="$t2">
        <so:extra><xsl:value-of select="$t2" /></so:extra>
      </xsl:when>
      </xsl:choose>
    </xsl:variable>
    <so:output>
      <xsl:copy-of select="exsl:node-set($t1)/so:output/* | exsl:node-set($t3)/so:output/*" />
    </so:output>
    <xsl:copy-of select="exsl:node-set($t3)/so:extra" />
  </xsl:when>
    <xsl:when test="$n">
      <so:extra><xsl:value-of select="$n" /></so:extra>
    </xsl:when>
  </xsl:choose>
</xsl:template>

<xsl:template name="array">
  <!-- Input like: [ X1 X2 ] bla -->
  <!-- output like: <so:output><Y>X1</Y><Y>X2</Y></so:output> <so:extra>}bla</so:extra> -->
  <xsl:param name="json-in" />
  <xsl:param name="parent-ele" />
  <xsl:variable name="t1" select="normalize-space(substring-after($json-in,'['))" />
  <xsl:variable name="t2">
    <xsl:call-template name="objects">
      <xsl:with-param name="json-in" select="$t1" />
      <xsl:with-param name="parent-ele" select="$parent-ele" />
    </xsl:call-template>
  </xsl:variable>  
  <xsl:variable name="t3" select="normalize-space(substring-after( exsl:node-set($t2)/so:extra, ']'))" />
  <xsl:copy-of select="exsl:node-set($t2)/so:output" />
  <xsl:if test="$t3">
    <so:extra><xsl:value-of select="$t3" /></so:extra>
  </xsl:if>  
</xsl:template>

<xsl:template name="value">
  <!-- Input like either array, object or string -->
  <!-- output like either array, object or string -->
  <xsl:param name="json-in" />
  <xsl:param name="parent-ele" />
  <xsl:variable name="first-letter" select="substring(normalize-space($json-in),1,1)" />
  <xsl:choose>
    <xsl:when test="$first-letter='{'">
    <xsl:call-template name="object">
        <xsl:with-param name="json-in" select="$json-in" />
        <xsl:with-param name="parent-ele" select="$parent-ele" />
    </xsl:call-template>
    </xsl:when>
    <xsl:when test="$first-letter='['">
    <xsl:call-template name="array">
        <xsl:with-param name="json-in" select="$json-in" />
        <xsl:with-param name="parent-ele" select="$parent-ele" />
    </xsl:call-template>
    </xsl:when>
    <xsl:when test="$first-letter=$quot">
    <xsl:call-template name="string">
        <xsl:with-param name="json-in" select="$json-in" />
        <xsl:with-param name="parent-ele" select="$parent-ele" />
    </xsl:call-template>
    </xsl:when>
  <xsl:otherwise>
    <so:output>ERROR</so:output>
  </xsl:otherwise>
  </xsl:choose>
</xsl:template>

<xsl:template name="string">
  <!-- Input like: "X" bla -->
  <!-- output like: <so:output><Y>X</Y></so:output> <so:extra>bla</so:extra> -->
  <xsl:param name="json-in" />
  <xsl:param name="parent-ele" />
  <xsl:variable name="value" select="substring-before(substring-after($json-in,$quot),$quot)" />
  <xsl:variable name="remainder" select="normalize-space(substring-after(substring-after($json-in,$quot),$quot))" />
  <so:output>
   <xsl:element name="{$parent-ele}">
    <xsl:value-of select="$value" />
   </xsl:element>
  </so:output>
  <xsl:if test="$remainder">
    <so:extra><xsl:value-of select="$remainder" /></so:extra>
  </xsl:if>  
</xsl:template>

</xsl:stylesheet>