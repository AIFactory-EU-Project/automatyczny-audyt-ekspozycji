<?php
/**
 * @license AiFactory
 */
declare(strict_types=1);

namespace App\Entity;

use DateTime;
use DateTimeInterface;
use Doctrine\ORM\Mapping as ORM;
use JMS\Serializer\Annotation as Serializer;

/**
 * @ORM\Entity(repositoryClass="App\Repository\AppLogRepository")
 * @ORM\Table(name="log", indexes={@ORM\Index(name="system_id_idx", columns={"system_id"})})
 * @ORM\HasLifecycleCallbacks
 *
 * @Serializer\ExclusionPolicy("ALL")
 */
class AppLog
{
    /**
     * @ORM\Id()
     * @ORM\GeneratedValue()
     * @ORM\Column(type="integer")

     * @Serializer\Groups({"list", "details"})
     */
    protected ?int $id = null;

    /**
     * @ORM\Column(name="message", type="text")
     */
    private ?string $message;

    /**
     * @ORM\Column(name="context", type="json")
     */
    private array $context = [];

    /**
     * @ORM\Column(name="level", type="smallint")
     */
    private ?int $level;

    /**
     * @ORM\Column(name="level_name", type="string", length=50)
     */
    private ?string $levelName;

    /**
     * @ORM\Column(name="extra", type="json")
     */
    private array $extra = [];

    /**
     * @ORM\Column(name="created_at", type="datetime")
     */
    private ?DateTimeInterface $createdAt;

    /**
     * @ORM\Column(type="integer")
     */
    private int $systemId = 0;

    /**
     * @ORM\PrePersist
     */
    public function onPrePersist()
    {
        $this->createdAt = new DateTime();
    }

    /**
     * @return int|null
     */
    public function getId(): ?int
    {
        return $this->id;
    }

    /**
     * @return string|null
     */
    public function getMessage(): ?string
    {
        return $this->message;
    }

    /**
     * @param string|null $message
     *
     * @return AppLog
     */
    public function setMessage(?string $message): AppLog
    {
        $this->message = $message;

        return $this;
    }

    /**
     * @return array
     */
    public function getContext(): array
    {
        return $this->context;
    }

    /**
     * @param array $context
     *
     * @return AppLog
     */
    public function setContext(array $context): AppLog
    {
        $this->context = $context;

        return $this;
    }

    /**
     * @return int|null
     */
    public function getLevel(): ?int
    {
        return $this->level;
    }

    /**
     * @param int|null $level
     *
     * @return AppLog
     */
    public function setLevel(?int $level): AppLog
    {
        $this->level = $level;

        return $this;
    }

    /**
     * @return string|null
     */
    public function getLevelName(): ?string
    {
        return $this->levelName;
    }

    /**
     * @param string|null $levelName
     *
     * @return AppLog
     */
    public function setLevelName(?string $levelName): AppLog
    {
        $this->levelName = $levelName;

        return $this;
    }

    /**
     * @return array
     */
    public function getExtra(): array
    {
        return $this->extra;
    }

    /**
     * @param array $extra
     *
     * @return AppLog
     */
    public function setExtra(array $extra): AppLog
    {
        $this->extra = $extra;

        return $this;
    }

    /**
     * @return DateTimeInterface|null
     */
    public function getCreatedAt(): ?DateTimeInterface
    {
        return $this->createdAt;
    }

    /**
     * @param DateTimeInterface|null $createdAt
     *
     * @return AppLog
     */
    public function setCreatedAt(?DateTimeInterface $createdAt): AppLog
    {
        $this->createdAt = $createdAt;

        return $this;
    }

    /**
     * @return int|null
     */
    public function getSystemId(): ?int
    {
        return $this->systemId;
    }

    /**
     * @param int $systemId
     *
     * @return $this
     */
    public function setSystemId(int $systemId): self
    {
        $this->systemId = $systemId;

        return $this;
    }
}
