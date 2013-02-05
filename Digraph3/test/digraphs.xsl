<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

<xsl:template match="digraph">
 <html>
  <head><title>Digraph XML implementation</title></head>
  <body>
   <h2>Digraph XML to HTML file converter</h2>
   <xsl:apply-templates/>
   <p>RB December 2006, version 1.0</p>
   </body>
  </html>
</xsl:template>

<xsl:template match="header">
   <h1><font color="#0000bb">XML stored digraph instance</font></h1>
   <table cellpadding="3">
   <xsl:apply-templates/>
   </table>
</xsl:template>

<xsl:template match="name">
   <tr><th align="left">Name: </th><th align="left"><font color="#0000bb"><xsl:apply-templates/></font></th></tr>
   <tr><th align="left">Category: </th><td><xsl:value-of select="/digraph/@category"/></td></tr>
   <tr><th align="left">Subcategory: </th><td><xsl:value-of select="/digraph/@subcategory"/></td></tr>
</xsl:template>

<xsl:template match="author">
   <tr><th align="left">Author: </th><td><xsl:apply-templates/></td></tr>
</xsl:template>

<xsl:template match="reference">
   <tr><th align="left">Reference: </th><td><em><xsl:apply-templates/></em></td></tr>
</xsl:template>

<xsl:template match="nodes">
   <h3><font color="#bb0000">Nodes</font></h3>
   <table border="1">
      <tr bgcolor="#9acd32">
        <th>Id.</th>
        <th>Name</th>
      </tr>
   <xsl:for-each select="node">
       <tr><td><xsl:number count="*" format="1"/></td>
           <td>&quot;<xsl:apply-templates/>&quot;</td></tr>
   </xsl:for-each>
   </table>
</xsl:template>

<xsl:template match="valuationdomain">   
   <h3><font color="#bb0000">Valuation domain</font></h3>
   <p>Minimum: <xsl:value-of select="min"/><br />
      Median : <xsl:value-of select="min + (max - min) div 2"/><br />
      Maximum: <xsl:value-of select="max"/>
   </p>
</xsl:template>

<xsl:template match="min">
	Minimum: <xsl:apply-templates/><br/>
</xsl:template>

<xsl:template match="max">
	Maximum: <xsl:apply-templates/>
</xsl:template>

<xsl:template match="relation">
   <xsl:variable name="Med" select="/digraph/valuationdomain/min + (/digraph/valuationdomain/max - /digraph/valuationdomain/min) div 2"/>
   <h3><font color="#bb0000">Relation</font></h3>
    <table border="1">
      <tr bgcolor="#9acd32">
        <th>Out</th>
        <th>In</th>
	<th>Value</th>
      </tr>
      <xsl:for-each select="arc">
      <tr>
        <td>&quot;<xsl:value-of select="i"/>&quot;</td>
        <td>&quot;<xsl:value-of select="t"/>&quot;</td>
      	<xsl:choose>
          <xsl:when test="v &gt; /digraph/valuationdomain/max">
            <td>Error: value too high</td>
          </xsl:when>
          <xsl:when test="v &lt; /digraph/valuationdomain/min">
            <td>Error: value too low</td>
          </xsl:when>
          <xsl:when test="v &gt; $Med">
            <td bgcolor="#ddffdd">
            <xsl:value-of select="v"/></td>
          </xsl:when>
          <xsl:when test="v &lt; $Med">
            <td bgcolor="#ffddff">
            <xsl:value-of select="v"/></td>
          </xsl:when>
          <xsl:otherwise>
            <td bgcolor="#dddddd">
            <xsl:value-of select="v"/></td>
          </xsl:otherwise>
        </xsl:choose>
      </tr>
      </xsl:for-each>
    </table>
</xsl:template>

</xsl:stylesheet>
