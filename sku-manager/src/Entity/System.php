<?php
/**
 * @license AiFactory
 */
declare(strict_types=1);

namespace App\Entity;

use DateTimeInterface;
use Doctrine\ORM\Mapping as ORM;
use JMS\Serializer\Annotation as Serializer;
use Symfony\Bridge\Doctrine\Validator\Constraints\UniqueEntity;
use Symfony\Component\Validator\Constraints as Assert;

/**
 * @ORM\Entity(repositoryClass="App\Repository\SystemRepository")
 *
 * @UniqueEntity("name")
 * @UniqueEntity("region")
 *
 * @Serializer\ExclusionPolicy("ALL")
 */
class System extends AbstractEntity
{
    /**
     * @ORM\Id()
     * @ORM\GeneratedValue()
     * @ORM\Column(type="integer")
     *
     * @Serializer\Groups({"list", "details"})
     */
    protected ?int $id = null;

    /**
     * @ORM\Column(type="datetime")
     *
     * @Serializer\Groups({"list", "details"})
     *
     * @Assert\NotBlank()
     */
    protected ?DateTimeInterface $createdDate = null;

    /**
     * @ORM\Column(type="datetime")
     *
     * @Serializer\Groups({"list", "details"})
     *
     * @Assert\NotBlank()
     */
    protected ?DateTimeInterface $updatedDate = null;

    /**
     * @ORM\Column(type="string", length=255, unique=true)
     *
     * @Assert\NotBlank()
     */
    private string $name;

    /**
     * @ORM\Column(type="datetime", nullable=true)
     */
    private ?DateTimeInterface $terminateDate = null;

    /**
     * @ORM\Column(type="string", length=255)
     *
     * @Assert\NotBlank()
     */
    private string $contact;

    /**
     * @ORM\Column(type="string", length=255, unique=true)
     *
     * @Assert\NotBlank()
     */
    private string $region;

    /**
     * @return string
     */
    public function getName(): string
    {
        return $this->name;
    }

    /**
     * @param string $name
     *
     * @return $this
     */
    public function setName(string $name): self
    {
        $this->name = $name;

        return $this;
    }

    public function getTerminateDate(): ?DateTimeInterface
    {
        return $this->terminateDate;
    }

    public function setTerminateDate(?DateTimeInterface $terminateDate): self
    {
        $this->terminateDate = $terminateDate;

        return $this;
    }

    public function getContact(): ?string
    {
        return $this->contact;
    }

    public function setContact(string $contact): self
    {
        $this->contact = $contact;

        return $this;
    }

    public function getRegion(): ?string
    {
        return $this->region;
    }

    public function setRegion(string $region): self
    {
        $this->region = $region;

        return $this;
    }
}
