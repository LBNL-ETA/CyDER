<?xml version="1.0" encoding="ISO-8859-1"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:output method="html" indent="yes" encoding="iso-8859-1"/>

<!-- To display treeview as expanded or minimized use external variable 'DefaultTreeMode' = 'expand' or 'minize'-->
<xsl:param name="DefaultTreeMode" select="'expand'"/>

<!-- _____ ITEM ________________________________________-->
<xsl:template match="item">

    <!-- REPORT ITEM (ROOT ITEM) -->
    <xsl:if test="count(ancestor::item)=0">
        <h1>RT-LAB Report</h1>
        <xsl:apply-templates select="item"/>
    </xsl:if>

    <!-- SECTION ITEM (SECOND LEVEL ITEM) -->
    <xsl:if test="(count(ancestor::item)=1)">
        
        <h2>
            <xsl:value-of select="concat(translate(substring(@name,1,1),'abcdefghijklmnopqrstuvwxyz','ABCDEFGHIJKLMNOPQRSTUVWXYZ'),substring(@name,2))"/>
        </h2>
        <hr class="hidescreen" style="border:1px" width="100%"/>
       
        <table class="hideprint" border="0" cellspacing="0" cellpadding="0">
            <col width="0%"/>
            <col width="0%"/>
            <col width="100%"/>
            <tbody>
                <tr>
                    <td>
                        <div class="bOut" onmouseover="swapClass(this, 'bOver')" onmouseout="swapClass(this, 'bOut')">
                            <xsl:attribute name="onclick">expandAllFromString('<xsl:value-of select="@name"/>')</xsl:attribute>
                            Expand
                        </div>
                    </td>
                    <td>
                        <div class="bOut" onmouseover="swapClass(this, 'bOver')" onmouseout="swapClass(this, 'bOut')">
                            <xsl:attribute name="onclick">collapseAllFromString('<xsl:value-of select="@name"/>')</xsl:attribute>                                                    
                        Minimize
                        </div>
                    </td>
                    <td>
                        <div class="bOut"><br/></div>
                    </td>
                </tr>
            </tbody>
        </table>
        <div style="padding-top: 8px;">
        <xsl:attribute name="id"><xsl:value-of select="@name"/></xsl:attribute>
        <xsl:apply-templates select="item"/>
        <xsl:apply-templates select="property"/>
        <xsl:apply-templates select="textlog"/>
        </div>
    </xsl:if>


    <!-- ITEM -->
    <xsl:if test="count(ancestor::item)&gt;1">
        <DIV CLASS="item" onclick="clickOnEntity(event, this);" onselectstart="return false" ondragstart="return false">

            <xsl:attribute name="id"><xsl:value-of select="@name"/></xsl:attribute>
            
            <!-- Add open attribute to DIV -->
            <xsl:choose>
                <xsl:when test="$DefaultTreeMode='minimize'">
                    <xsl:attribute name="open">false</xsl:attribute>
                </xsl:when>
                <xsl:otherwise>
                    <xsl:attribute name="open">true</xsl:attribute>
                </xsl:otherwise>
            </xsl:choose>
           
            <!-- Add style attribute to DIV -->
            <xsl:attribute name="STYLE">
                padding-left: 20px;
                cursor: pointer;
                <xsl:if test="(count(ancestor::item)&gt;2) and ($DefaultTreeMode='minimize')">
                    display: none;
                </xsl:if>
            </xsl:attribute>

            <!-- Add openImage attribute to DIV -->
            <xsl:attribute name="openImage">images/openitem.gif</xsl:attribute>
            
            <!-- Add closeImage attribute to DIV -->
            <xsl:attribute name="closeImage">images/closeitem.gif</xsl:attribute>

            <!-- Add table -->  
            <table border="0" cellspacing="0" cellpadding="0">
            
                <!-- Add row to the table -->
                <tr>
                
                    <!-- Add cell element to the row -->
                    <td valign="middle">
                    
                        <!-- Add image to the cell -->

                        <xsl:choose>
                            <xsl:when test="$DefaultTreeMode='minimize'">
                                <img border="0" id="image" SRC="images/closeitem.gif">
                                </img>
                            </xsl:when>
                            <xsl:otherwise>
                                <img border="0" id="image" SRC="images/openitem.gif">
                                </img>
                            </xsl:otherwise>
                        </xsl:choose>                        
                    </td>
                    
                    <!-- Add cell element to the row -->
                    <td valign="middle"
                        nowrap="true"
                        class="notsel"
                        onmouseover="swapClass(this, 'sel')"
                        onmouseout="swapClass(this, 'notsel')">
                        <!-- Add text to the cell -->
                        <xsl:value-of select="@name"/>
                    </td>
                </tr>
            </table>
            
            <!-- Display sub element -->
            <xsl:apply-templates select="item"/>
            <xsl:apply-templates select="property"/>
            <xsl:apply-templates select="textlog"/>

        </DIV>
    </xsl:if>
</xsl:template>

<!-- PROPERTY -->
<xsl:template match="property">
  <DIV CLASS="property" onclick="cancelBuble(event);" onselectstart="return false" ondragstart="return false">
  
    <!-- Add open attribute to DIV -->
    <xsl:choose>
        <xsl:when test="$DefaultTreeMode='minimize'">
            <xsl:attribute name="open">false</xsl:attribute>
        </xsl:when>
        <xsl:otherwise>
            <xsl:attribute name="open">true</xsl:attribute>
        </xsl:otherwise>
    </xsl:choose>
    
    <!-- Add style attribute to DIV -->
    <xsl:attribute name="STYLE">
      padding-left: 20px;
      cursor: pointer;
      <xsl:if test="(count(ancestor::item)&gt;2) and ($DefaultTreeMode='minimize')">
        display: none;
      </xsl:if>
    </xsl:attribute>

    <!-- Add table -->  
    <table border="0" cellspacing="0" cellpadding="0">
    
      <!-- Add row to the table -->
      <tr>
      
        <!-- Add cell element to the row -->
        <td valign="middle">
        
          <!-- Add image to the cell -->
          <img border="0" id="image" SRC="images/property.gif">
          </img>
        </td>
        
        <!-- Add cell element to the row -->
        <td valign="middle"
            class="notsel"
            onmouseover="swapClass(this, 'sel')"
            onmouseout="swapClass(this, 'notsel')"        
            nowrap="true">
            
          <!-- Add text to the cell -->
          <xsl:if test="not(translate(@name,' ','')='')">
              <xsl:value-of select="@name"/>=
          </xsl:if>
          <xsl:value-of select="value"/>
          
        </td>
      </tr>
    </table>
  </DIV>
</xsl:template>

<!-- TEXTLOG -->
<xsl:template match="textlog">
  <DIV CLASS="textlog" onclick="cancelBuble(event);" onselectstart="cancelBuble(event);" ondragstart="return false">
    <!-- Add open attribute to DIV -->
    <xsl:choose>
        <xsl:when test="$DefaultTreeMode='minimize'">
            <xsl:attribute name="open">false</xsl:attribute>
        </xsl:when>
        <xsl:otherwise>
            <xsl:attribute name="open">true</xsl:attribute>
        </xsl:otherwise>
    </xsl:choose>

    
    <!-- Add style attribute to DIV -->
    <xsl:attribute name="STYLE">
      padding-left: 20px;
      cursor: text;
      <xsl:if test="(count(ancestor::item)&gt;2) and ($DefaultTreeMode='minimize')">
        display: none;
      </xsl:if>
    </xsl:attribute>

    <!-- Add section -->

    <table>
    <div style="padding-top: 4px; padding-right: 10px;" onselectstart="return true;">
		<!-- Display log file -->
		<pre><xsl:call-template name="string-trim">
			<xsl:with-param name="string" select="."/>
		</xsl:call-template></pre>
    </div>
    </table>
  </DIV>
</xsl:template>

<xsl:variable name="whitespace" select="'&#09;&#10;&#13; '" />
<!-- Strips trailing whitespace characters from 'string' -->
<xsl:template name="string-rtrim">
    <xsl:param name="string" />
    <xsl:param name="trim" select="$whitespace" />

    <xsl:variable name="length" select="string-length($string)" />

    <xsl:if test="$length &gt; 0">
        <xsl:choose>
            <xsl:when test="contains($trim, substring($string, $length, 1))">
                <xsl:call-template name="string-rtrim">
                    <xsl:with-param name="string" select="substring($string, 1, $length - 1)" />
                    <xsl:with-param name="trim"   select="$trim" />
                </xsl:call-template>
            </xsl:when>
            <xsl:otherwise>
                <xsl:value-of select="$string" />
            </xsl:otherwise>
        </xsl:choose>
    </xsl:if>
</xsl:template>
<!-- Strips leading whitespace characters from 'string' -->
<xsl:template name="string-ltrim">
    <xsl:param name="string" />
    <xsl:param name="trim" select="$whitespace" />

    <xsl:if test="string-length($string) &gt; 0">
        <xsl:choose>
            <xsl:when test="contains($trim, substring($string, 1, 1))">
                <xsl:call-template name="string-ltrim">
                    <xsl:with-param name="string" select="substring($string, 2)" />
                    <xsl:with-param name="trim"   select="$trim" />
                </xsl:call-template>
            </xsl:when>
            <xsl:otherwise>
                <xsl:value-of select="$string" />
            </xsl:otherwise>
        </xsl:choose>
    </xsl:if>
</xsl:template>
<!-- Strips leading and trailing whitespace characters from 'string' -->
<xsl:template name="string-trim">
    <xsl:param name="string" />
    <xsl:param name="trim" select="$whitespace" />
    <xsl:call-template name="string-rtrim">
        <xsl:with-param name="string">
            <xsl:call-template name="string-ltrim">
                <xsl:with-param name="string" select="$string" />
                <xsl:with-param name="trim"   select="$trim" />
            </xsl:call-template>
        </xsl:with-param>
        <xsl:with-param name="trim"   select="$trim" />
    </xsl:call-template>
</xsl:template>

</xsl:stylesheet>