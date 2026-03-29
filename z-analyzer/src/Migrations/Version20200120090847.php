<?php

declare(strict_types=1);

namespace DoctrineMigrations;

use Doctrine\DBAL\Schema\Schema;
use Doctrine\Migrations\AbstractMigration;

/**
 * Auto-generated Migration: Please modify to your needs!
 */
final class Version20200120090847 extends AbstractMigration
{
    public function getDescription() : string
    {
        return '';
    }

    public function up(Schema $schema) : void
    {
        // this up() migration is auto-generated, please modify it to your needs
        $this->abortIf($this->connection->getDatabasePlatform()->getName() !== 'postgresql', 'Migration can only be executed safely on \'postgresql\'.');

        $this->addSql('ALTER TABLE report_photo_analysis ADD real_photo_id INT DEFAULT NULL');
        $this->addSql('ALTER TABLE report_photo_analysis ADD CONSTRAINT FK_C38374C789FB2411 FOREIGN KEY (real_photo_id) REFERENCES photo (id) NOT DEFERRABLE INITIALLY IMMEDIATE');
        $this->addSql('CREATE UNIQUE INDEX UNIQ_C38374C789FB2411 ON report_photo_analysis (real_photo_id)');
    }

    public function down(Schema $schema) : void
    {
        // this down() migration is auto-generated, please modify it to your needs
        $this->abortIf($this->connection->getDatabasePlatform()->getName() !== 'postgresql', 'Migration can only be executed safely on \'postgresql\'.');

        $this->addSql('CREATE SCHEMA public');
        $this->addSql('ALTER TABLE report_photo_analysis DROP CONSTRAINT FK_C38374C789FB2411');
        $this->addSql('DROP INDEX UNIQ_C38374C789FB2411');
        $this->addSql('ALTER TABLE report_photo_analysis DROP real_photo_id');
    }
}
