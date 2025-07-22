-- Initialize database for Lovable clone
CREATE TABLE IF NOT EXISTS websites (
    id INT AUTO_INCREMENT PRIMARY KEY,
    prompt TEXT NOT NULL,
    files_generated JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS prompt_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    website_id INT,
    prompt_text TEXT NOT NULL,
    prompt_type ENUM('initial', 'refinement') DEFAULT 'initial',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (website_id) REFERENCES websites(id) ON DELETE CASCADE
);

-- Insert sample data
