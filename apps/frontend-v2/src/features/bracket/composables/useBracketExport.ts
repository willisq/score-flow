import { jsPDF } from "jspdf";
import html2canvas from "html2canvas";

export function useBracketExport() {
  const logoUrl = "/img/logo.jpeg";
  let cachedLogoBase64: string | null = null;

  const loadLogo = async (): Promise<string | null> => {
    if (cachedLogoBase64) return cachedLogoBase64;
    try {
      const response = await fetch(logoUrl);
      const blob = await response.blob();
      return new Promise((resolve) => {
        const reader = new FileReader();
        reader.onloadend = () => {
          cachedLogoBase64 = reader.result as string;
          resolve(cachedLogoBase64);
        };
        reader.readAsDataURL(blob);
      });
    } catch (error) {
      console.error("Error loading logo:", error);
      return null;
    }
  };

  const captureElement = async (elementId: string) => {
    const element = document.getElementById(elementId);
    if (!element) {
      console.error("Element not found:", elementId);
      return null;
    }

    const canvas = await html2canvas(element, {
      scale: 1.3,
      useCORS: true,
      backgroundColor: "#ffffff",
      logging: false,
    });
    return canvas.toDataURL("image/jpeg", 0.7);
  };

  const addBracketToPdf = (pdf: jsPDF, imgData: string, category: any, logoBase64: string | null) => {
    const pageWidth = pdf.internal.pageSize.getWidth();
    const pageHeight = pdf.internal.pageSize.getHeight();
    const margin = 15;

    // Logo in Header (Right side)
    if (logoBase64) {
      const logoSize = 22;
      pdf.addImage(logoBase64, "PNG", pageWidth - margin - logoSize, 7, logoSize, logoSize, undefined, "FAST");
    }

    // Special Condition Label (Below logo area)
    if (category.isSpecial) {
      pdf.setFillColor(245, 245, 245);
      pdf.setDrawColor(200);
      pdf.roundedRect(pageWidth - margin - 45, 30, 45, 6, 1, 1, "FD");
      pdf.setFontSize(8);
      pdf.setTextColor(80);
      pdf.setFont("helvetica", "bold");
      pdf.text("CONDICIÓN ESPECIAL", pageWidth - margin - 22.5, 34, { align: "center" });
    }

    // Header Information (Left side)
    pdf.setFontSize(18);
    pdf.setTextColor(40);
    pdf.setFont("helvetica", "bold");
    pdf.text(category.modalityName || "Pirámide de Competencia", margin, 20);

    pdf.setFontSize(10);
    pdf.setTextColor(100);
    pdf.setFont("helvetica", "normal");
    const details = `${category.ageStr} | ${category.sexesStr} | ${category.ranksStr}${category.weightStr ? " | " + category.weightStr : ""}`;
    pdf.text(details, margin, 28);

    // Separator line
    pdf.setDrawColor(220);
    pdf.setLineWidth(0.2);
    pdf.line(margin, 38, pageWidth - margin, 38);

    // Common footer metrics
    const footerHeight = 45;
    const footerY = pageHeight - footerHeight + 10;

    // Table Info Section (Bottom Left)
    pdf.setFontSize(11);
    pdf.setTextColor(40);
    pdf.setFont("helvetica", "bold");
    pdf.text("CONTROL DE MESA:", margin, footerY);

    pdf.setFont("helvetica", "normal");
    pdf.setFontSize(10);
    
    // Row 1: Mesa #
    pdf.text("Mesa #:", margin, footerY + 12);
    pdf.setDrawColor(180);
    pdf.line(margin + 15, footerY + 13, margin + 40, footerY + 13);

    // Row 2: Director(a) de mesa
    const row2Y = footerY + 22;
    pdf.text("Director(a) de mesa:", margin, row2Y);
    pdf.line(margin + 35, row2Y + 1, margin + 95, row2Y + 1);

    // Winners Section (Bottom Right)
    const sectionWidth = 100;
    const sectionX = pageWidth - margin - sectionWidth;
    
    pdf.setFontSize(11);
    pdf.setTextColor(40);
    pdf.setFont("helvetica", "bold");
    pdf.text("GANADORES DE LA CATEGORÍA:", sectionX, footerY);
    
    pdf.setFont("helvetica", "normal");
    pdf.setFontSize(10);
    const labelWidth = 22;
    const lineStartX = sectionX + labelWidth;
    const lineEndX = pageWidth - margin;
    const labels = ["1er Lugar:", "2do Lugar:", "3er Lugar:"];
    
    labels.forEach((label, i) => {
      const y = footerY + 12 + (i * 10);
      pdf.text(label, sectionX, y);
      pdf.setDrawColor(180);
      pdf.line(lineStartX, y + 1, lineEndX, y + 1);
    });

    // Image metrics
    const imgProps = pdf.getImageProperties(imgData);
    const maxContentWidth = pageWidth - 2 * margin;
    const maxContentHeight = pageHeight - 42 - footerHeight - 5;

    // Use a fixed pixels-to-mm ratio so all brackets have the same card size
    let finalWidth = imgProps.width / 3.8;
    
    if (finalWidth > maxContentWidth) {
      finalWidth = maxContentWidth;
    }
    
    let finalHeight = (imgProps.height * finalWidth) / imgProps.width;
    
    if (finalHeight > maxContentHeight) {
      finalHeight = maxContentHeight;
      finalWidth = (imgProps.width * finalHeight) / imgProps.height;
    }

    const xPos = margin; // Left aligned
    pdf.addImage(imgData, "JPEG", xPos, 45, finalWidth, finalHeight, undefined, "FAST");
  };

  const exportToPdf = async (elementId: string, category: any) => {
    try {
      const [imgData, logoBase64] = await Promise.all([
        captureElement(elementId),
        loadLogo()
      ]);
      
      if (!imgData) return;

      const pdf = new jsPDF({
        orientation: category.orientation || "landscape",
        unit: "mm",
        format: "letter",
      });

      addBracketToPdf(pdf, imgData, category, logoBase64);

      const fileName = `Piramide_${category.modalityName.replace(/\s+/g, "_")}_${category.ranksStr.replace(/\s+/g, "_")}.pdf`;
      pdf.save(fileName);
    } catch (error) {
      console.error("Error generating PDF:", error);
    }
  };

  const exportAllToPdf = async (groups: any[]) => {
    try {
      if (groups.length === 0) return;

      const logoBase64 = await loadLogo();

      const pdf = new jsPDF({
        orientation: groups[0].orientation || "landscape",
        unit: "mm",
        format: "letter",
      });

      for (let i = 0; i < groups.length; i++) {
        const group = groups[i];
        if (!group.elementId) continue;

        const imgData = await captureElement(group.elementId);
        if (!imgData) continue;

        if (i > 0) {
          pdf.addPage("letter", group.orientation || "landscape");
        }

        addBracketToPdf(pdf, imgData, group, logoBase64);
      }

      pdf.save("Reporte_Global_Piramides.pdf");
    } catch (error) {
      console.error("Error generating Global PDF:", error);
    }
  };

  return {
    exportToPdf,
    exportAllToPdf,
  };
}
