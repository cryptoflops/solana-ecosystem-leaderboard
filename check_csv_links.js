const fs = require('fs');
const path = require('path');

function parseCSVLine(line) {
  const result = [];
  let current = '';
  let inQuotes = false;
  
  for (let i = 0; i < line.length; i++) {
    const char = line[i];
    if (char === '"') {
      inQuotes = !inQuotes;
    } else if (char === ',' && !inQuotes) {
      result.push(current);
      current = '';
    } else {
      current += char;
    }
  }
  result.push(current);
  return result;
}

function main() {
  const csvPath = 'user/solana-twitter-research/solana_influential_accounts.csv';
  const content = fs.readFileSync(csvPath, 'utf8');
  const lines = content.split('\n').filter(l => l.trim() !== "");
  const headers = parseCSVLine(lines[0]);
  
  console.log(`Checking ${lines.length - 1} accounts...`);
  
  const handles = new Set();
  const duplicateHandles = [];
  const invalidLinks = [];
  
  for (let i = 1; i < lines.length; i++) {
    const values = parseCSVLine(lines[i]);
    const row = {};
    for (let j = 0; j < headers.length; j++) {
      row[headers[j].trim()] = values[j] ? values[j].trim() : "";
    }
    
    const link = row["Twitter Link"];
    const name = row["Name"];
    
    if (!link) {
      invalidLinks.push({ line: i + 1, name, error: "Empty link" });
      continue;
    }
    
    // Check for weird characters (non-ASCII)
    const nonAscii = /[^\x00-\x7F]/.test(link);
    if (nonAscii) {
      const asciiCodes = [];
      for(let k=0; k<link.length; k++) {
        if(link.charCodeAt(k) > 127) {
          asciiCodes.push(`${link[k]} (${link.charCodeAt(k)})`);
        }
      }
      invalidLinks.push({ line: i + 1, name, link, error: `Contains non-ASCII characters: ${asciiCodes.join(', ')}` });
    }
    
    // Check URL structure
    if (!link.startsWith("https://x.com/") && !link.startsWith("https://twitter.com/")) {
      invalidLinks.push({ line: i + 1, name, link, error: "Invalid URL prefix (must be https://x.com/ or https://twitter.com/)" });
    }
    
    // Check for spaces or trailing symbols
    if (/\s/.test(link)) {
      invalidLinks.push({ line: i + 1, name, link, error: "Contains spaces" });
    }
    
    // Extract handle
    let handle = "";
    const match = link.match(/(?:x|twitter)\.com\/([a-zA-Z0-9_]+)/i);
    if (match) {
      handle = '@' + match[1].toLowerCase();
      if (handles.has(handle)) {
        duplicateHandles.push({ name, handle, link });
      } else {
        handles.add(handle);
      }
    } else {
      invalidLinks.push({ line: i + 1, name, link, error: "Could not parse handle from URL" });
    }
  }
  
  console.log("\n--- INVALID LINKS REPORT ---");
  if (invalidLinks.length === 0) {
    console.log("No syntax or non-ASCII errors found in links!");
  } else {
    invalidLinks.forEach(err => {
      console.log(`Line ${err.line} (${err.name}): ${err.error} - URL: "${err.link}"`);
    });
  }
  
  console.log("\n--- DUPLICATE HANDLES REPORT ---");
  if (duplicateHandles.length === 0) {
    console.log("No duplicate handles found!");
  } else {
    duplicateHandles.forEach(dup => {
      console.log(`Duplicate found: ${dup.name} (${dup.handle}) - Link: ${dup.link}`);
    });
  }
}

main();
