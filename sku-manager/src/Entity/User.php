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
use Symfony\Component\Security\Core\User\UserInterface;
use Symfony\Component\Validator\Constraints as Assert;

/**
 * @Orm\Table("`user`")
 *
 * @ORM\Entity(repositoryClass="App\Repository\UserRepository")
 *
 * @UniqueEntity("email")
 *
 * @Serializer\ExclusionPolicy("ALL")
 */
class User extends AbstractEntity implements UserInterface
{
    /**
     * @ORM\Id()
     * @ORM\GeneratedValue()
     * @ORM\Column(type="integer")
     *
     * @Serializer\Expose()
     * @Serializer\Groups({"list", "details"})
     */
    protected ?int $id = null;

    /**
     * @ORM\Column(type="datetime")
     *
     * @Serializer\Expose()
     *
     * @Assert\NotBlank()
     */
    protected ?DateTimeInterface $createdDate = null;

    /**
     * @ORM\Column(type="datetime")
     *
     * @Serializer\Expose()
     *
     * @Assert\NotBlank()
     */
    protected ?DateTimeInterface $updatedDate = null;

    /**
     * @ORM\ManyToOne(targetEntity="App\Entity\System", inversedBy="users")
     * @ORM\JoinColumn(nullable=false)
     *
     * @Assert\NotBlank()
     */
    private ?System $system = null;

    /**
     * @ORM\Column(type="string", length=180, unique=true)
     *
     * @Serializer\Expose()
     * @Serializer\Groups({"list", "details"})
     *
     * @Assert\NotBlank()
     * @Assert\Email()
     */
    private string $email = '';

    /**
     * @ORM\Column(type="json")
     *
     * @Serializer\Expose()
     *
     * @var string[]
     */
    private array $roles = [];

    /**
     * @ORM\Column(type="string")
     */
    private string $password = '';

    private ?string $plainPassword = null;

    /**
     * @ORM\Column(type="datetime", nullable=true)
     */
    private ?DateTimeInterface $passwordRequestedAt = null;

    /**
     * @ORM\Column(type="string", length=255, nullable=true)
     */
    private ?string $confirmationToken = null;

    /**
     * @ORM\Column(type="integer", nullable=true)
     */
    private ?int $failedAttempts = 0;

    /**
     * @return System
     */
    public function getSystem(): ?System
    {
        return $this->system;
    }

    /**
     * @param System $system
     *
     * @return $this
     */
    public function setSystem(System $system): self
    {
        $this->system = $system;

        return $this;
    }

    /**
     * @return string
     */
    public function getEmail(): string
    {
        return $this->email;
    }

    /**
     * @param string $email
     *
     * @return $this
     */
    public function setEmail(string $email): self
    {
        $this->email = $email;

        return $this;
    }

    /**
     * A visual identifier that represents this user.
     *
     * @return string
     *
     * @see UserInterface
     */
    public function getUsername(): string
    {
        return $this->email;
    }

    /**
     * @return string[]
     *
     * @see UserInterface
     */
    public function getRoles(): array
    {
        $roles = $this->roles;
        // guarantee every user at least has ROLE_USER
        $roles[] = 'ROLE_USER';

        return array_unique($roles);
    }

    /**
     * @param array $roles
     *
     * @return $this
     */
    public function setRoles(array $roles): self
    {
        $this->roles = $roles;

        return $this;
    }

    /**
     * @return string
     */
    public function getPassword(): string
    {
        return $this->password;
    }

    /**
     * @param string $password
     *
     * @return $this
     */
    public function setPassword(string $password): self
    {
        $this->password = $password;

        return $this;
    }

    /**
     * @param string $plainPassword
     */
    public function setPlainPassword(?string $plainPassword): void
    {
        $this->plainPassword = $plainPassword;
    }

    /**
     * @return string|null
     */
    public function getPlainPassword(): ?string
    {
        return $this->plainPassword;
    }

    /**
     * @see UserInterface
     *
     * @return null
     */
    public function getSalt()
    {
        return null; // not needed when using the "bcrypt" algorithm in security.yaml
    }

    /**
     * @see UserInterface
     */
    public function eraseCredentials()
    {
        $this->plainPassword = null;
    }

    /**
     * @return DateTimeInterface|null
     */
    public function getPasswordRequestedAt(): ?DateTimeInterface
    {
        return $this->passwordRequestedAt;
    }

    /**
     * @param DateTimeInterface|null $passwordRequestedAt
     *
     * @return $this
     */
    public function setPasswordRequestedAt(?DateTimeInterface $passwordRequestedAt): self
    {
        $this->passwordRequestedAt = $passwordRequestedAt;

        return $this;
    }

    /**
     * @return string|null
     */
    public function getConfirmationToken(): ?string
    {
        return $this->confirmationToken;
    }

    /**
     * @param string|null $confirmationToken
     *
     * @return $this
     */
    public function setConfirmationToken(?string $confirmationToken): self
    {
        $this->confirmationToken = $confirmationToken;

        return $this;
    }

    public function getFailedAttempts(): ?int
    {
        return $this->failedAttempts;
    }

    public function setFailedAttempts(int $failedAttempts): self
    {
        $this->failedAttempts = $failedAttempts;

        return $this;
    }

    public function addRole(string $role): void
    {
        $roles = $this->getRoles();
        $roles[] = $role;
        $this->setRoles(array_unique($roles));
    }
}
