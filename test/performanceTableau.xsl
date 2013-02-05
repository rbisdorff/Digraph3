<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

<xsl:template match="performancetableau">
 <html>
  <head><title>Digraph XML implementation</title></head>
  <body>
   <h2>Digraph XML to HTML converter</h2>
   <xsl:apply-templates/>
   <p>RB February 2007, version 1.0</p>
   </body>
  </html>
</xsl:template>

<xsl:template match="header">
   <h1><font color="#0000bb">Stored performance tableau instance</font></h1>
   <table cellpadding="3">
   <xsl:apply-templates/>
   </table>
</xsl:template>

<xsl:template match="name">
   <tr><th align="left">Name: </th><th align="left"><font color="#0000bb"><xsl:apply-templates/></font></th></tr>
   <tr><th align="left">Category: </th><td><xsl:value-of select="/performancetableau/@category"/></td></tr>
   <tr><th align="left">Subcategory: </th><td><xsl:value-of select="/performancetableau/@subcategory"/></td></tr>
</xsl:template>

<xsl:template match="author">
   <tr><th align="left">Author: </th><td><xsl:apply-templates/></td></tr>
</xsl:template>

<xsl:template match="reference">
   <tr><th align="left">Reference: </th><td><em><xsl:apply-templates/></em></td></tr>
</xsl:template>

<xsl:template match="criteria">
   <h3><font color="#bb0000">Criteria</font></h3>
   <table border="1">
     <tr bgcolor="#9acd32">
        <th rowspan="2">Id.</th>
        <th rowspan="2">Name</th>
        <th rowspan="2">Weight</th>
	<th rowspan="2">Scale</th>
	<th colspan="4">Thresholds</th>
     </tr>
     <tr bgcolor="#9acd32">
	<th>Indifference</th>
	<th>Preference</th>
	<th>Weak veto</th>
	<th>Veto</th>
      </tr>
   <xsl:for-each select="criterion">
       <tr><th><xsl:number count="*" format="1"/></th>
           <td>&quot;<xsl:value-of select="critname"/>&quot;</td>
	   <td><xsl:value-of select="weight"/></td>
	   <td>(<xsl:value-of select="scale/min"/>,<xsl:value-of select="scale/max"/>)</td>
	   <td align="center"><xsl:value-of select="thresholds/indifference"/></td>
	   <td align="center"><xsl:value-of select="thresholds/preference"/></td>
	   <td align="center"><xsl:value-of select="thresholds/weakveto"/></td>
	   <td align="center"><xsl:value-of select="thresholds/veto"/></td></tr>          
   </xsl:for-each>
   </table>
</xsl:template>

<xsl:template match="actions">
   <h3><font color="#bb0000">Actions</font></h3>
   <table border="1">
      <tr bgcolor="#9acd32">
        <th>Id.</th>
        <th>Name</th>
      </tr>
   <xsl:for-each select="action">
       <tr><th><xsl:number count="*" format="1"/></th>
           <td>&quot;<xsl:apply-templates/>&quot;</td>
       </tr>
   </xsl:for-each>
   </table>
</xsl:template>



<xsl:template match="evaluations">
   <h3><font color="#bb0000">Performance Tableau</font></h3>
    <table border="1">
      <tr bgcolor="#9acd32">
        <th>Criterion\Action</th>
	<xsl:for-each select="/performancetableau/actions/action">
	  <th><xsl:apply-templates/></th>
        </xsl:for-each>
      </tr>
      <xsl:apply-templates/>
    </table>
</xsl:template>

<xsl:template match="evaluation">
  <tr>
    <th>&quot;<xsl:value-of select="critname"/>&quot;</th>
    <xsl:for-each select="evalactions">
      <td><xsl:value-of select="value"/></td>
    </xsl:for-each> 
  </tr>
</xsl:template>

</xsl:stylesheet>

